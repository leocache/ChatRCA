import pandas as pd
import numpy as np
import os
import re
import datetime
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models.fasttext import FastText
from sklearn.model_selection import train_test_split


class RCASystem:
    def __init__(self, base_dir='./TrainTicket', alpha=0.3, k=5, model_path=None):
        """
        Initialize the RCA system

        Args:
            base_dir: Directory containing fault folders (default: './TrainTicket')
            alpha: Weight for time decay factor in similarity calculation
            k: Number of similar historical events to consider
            model_path: Path to save/load FastText model (optional)
        """
        self.base_dir = base_dir
        self.alpha = alpha
        self.k = k
        self.fasttext_model = None
        self.model_path = model_path
        self.historical_events = []
        self.historical_labels = []
        # 添加故障类型映射
        self.fault_type_mapping = {
            1: 'Return',
            2: 'Exception',
            3: 'Network Delay',
            4: 'CPU Contention'
        }

    def load_data(self, fault_dirs=None):
        """
        Load data from all fault directories

        Args:
            fault_dirs: List of fault directory names, if None load all
        """
        if not os.path.exists(self.base_dir):
            raise ValueError(f"目录 {self.base_dir} 不存在，请确保TrainTicket文件夹与fasttext.py在同一目录下")

        if fault_dirs is None:
            # Assuming directory structure with fault1, fault2, etc.
            fault_dirs = [d for d in os.listdir(self.base_dir) if d.startswith('fault')]

        if not fault_dirs:
            raise ValueError(f"在目录 {self.base_dir} 中没有找到任何故障文件夹（fault*）")

        print(f"找到以下故障文件夹：{', '.join(fault_dirs)}")

        for fault_dir in fault_dirs:
            fault_path = os.path.join(self.base_dir, fault_dir)
            if not os.path.isdir(fault_path):
                continue

            # Extract fault number as the label
            fault_label = re.search(r'fault_?(\d+)', fault_dir)  # 允许下划线存在或不存在
            if fault_label:
                fault_num = int(fault_label.group(1))
            else:
                continue

            # Load logs, traces and metrics
            log_path = os.path.join(fault_path, 'log.csv')
            trace_path = os.path.join(fault_path, 'trace.csv')
            metric_path = os.path.join(fault_path, 'metric.csv')

            if os.path.exists(log_path) and os.path.exists(trace_path) and os.path.exists(metric_path):
                try:
                    event_data = self.extract_event_features(log_path, trace_path, metric_path)
                    event_text = self.event_to_text(event_data)
                    timestamp = self.extract_timestamp(event_data)

                    self.historical_events.append({
                        'text': event_text,
                        'data': event_data,
                        'timestamp': timestamp,
                        'label': fault_num
                    })
                    self.historical_labels.append(fault_num)
                    print(f"成功加载故障 {fault_num} 的数据")
                except Exception as e:
                    print(f"加载故障 {fault_num} 数据时出错：{str(e)}")
            else:
                print(f"警告：故障 {fault_num} 的数据文件不完整")

        if not self.historical_events:
            raise ValueError("没有成功加载任何故障数据，请检查数据文件是否完整")

        print(f"成功加载 {len(self.historical_events)} 个历史故障事件")
        return self.historical_events

    def extract_event_features(self, log_path, trace_path, metric_path):
        """
        Extract features from log, trace and metric files

        Args:
            log_path: Path to log.csv
            trace_path: Path to trace.csv
            metric_path: Path to metric.csv

        Returns:
            Dictionary containing extracted features
        """
        # Load data
        logs = pd.read_csv(log_path)
        traces = pd.read_csv(trace_path)
        metrics = pd.read_csv(metric_path)

        # Clean metrics data (remove empty rows)
        metrics = metrics.dropna(how='all')

        event_data = {
            'logs': logs,
            'traces': traces,
            'metrics': metrics
        }

        return event_data

    def extract_timestamp(self, event_data):
        """
        Extract timestamp from event data

        Args:
            event_data: Dictionary with logs, traces, metrics dataframes

        Returns:
            Timestamp for the event
        """
        # Extract timestamp from logs if available
        if not event_data['logs'].empty and 'TimeUnixNano' in event_data['logs'].columns:
            timestamp = event_data['logs']['TimeUnixNano'].min() / 1e9  # Convert to seconds
            return timestamp

        # Or use trace data
        if not event_data['traces'].empty and 'StartTimeUnixNano' in event_data['traces'].columns:
            timestamp = event_data['traces']['StartTimeUnixNano'].min() / 1e9
            return timestamp

        # Fallback to metric data
        if not event_data['metrics'].empty and 'TimeStamp' in event_data['metrics'].columns:
            valid_timestamps = event_data['metrics']['TimeStamp'].dropna()
            if not valid_timestamps.empty:
                return valid_timestamps.min()

        # Default to current time if no timestamp found
        return datetime.datetime.now().timestamp()

    def event_to_text(self, event_data):
        """
        Convert event data to text representation for FastText

        Args:
            event_data: Dictionary with logs, traces, metrics dataframes

        Returns:
            Text representation of the event
        """
        text_parts = []

        # Extract log messages
        if not event_data['logs'].empty and 'Log' in event_data['logs'].columns:
            log_texts = event_data['logs']['Log'].dropna().tolist()
            text_parts.extend([f"LOG: {log}" for log in log_texts])

        # Extract trace operations
        if not event_data['traces'].empty and 'OperationName' in event_data['traces'].columns:
            trace_ops = event_data['traces']['OperationName'].dropna().tolist()
            text_parts.extend([f"TRACE: {op}" for op in trace_ops])

        # Extract pod names and anomalous metrics
        if not event_data['metrics'].empty:
            if 'PodName' in event_data['metrics'].columns and 'CpuUsageRate(%)' in event_data['metrics'].columns:
                for idx, row in event_data['metrics'].iterrows():
                    if pd.notna(row['PodName']) and pd.notna(row['CpuUsageRate(%)']):
                        text_parts.append(
                            f"METRIC: {row['PodName']} CPU {row['CpuUsageRate(%)']} MEM {row.get('MemoryUsageRate(%)', 'N/A')}")

        return " ".join(text_parts)

    def train_fasttext_model(self, min_count=1, vector_size=100, window=5, sg=1, epochs=20, force_retrain=False):
        """
        Train a FastText model on historical event texts

        Args:
            min_count: Minimum word count threshold
            vector_size: Size of word vectors
            window: Maximum distance between current and predicted word
            sg: Training algorithm: 1 for skip-gram; otherwise CBOW
            epochs: Number of iterations over the corpus
            force_retrain: If True, force retraining even if model exists
        """
        if not self.historical_events:
            raise ValueError("没有历史事件数据，无法训练模型")

        # 检查是否已有模型且无需强制重新训练
        if self.fasttext_model is not None and not force_retrain:
            print("FastText模型已存在，跳过训练")
            return self.fasttext_model

        # 如果指定了 model_path 且模型文件存在，则加载现有模型
        if self.model_path and os.path.exists(self.model_path) and not force_retrain:
            try:
                self.fasttext_model = FastText.load(self.model_path)
                print(f"从 {self.model_path} 加载现有FastText模型")
                return self.fasttext_model
            except Exception as e:
                print(f"加载模型失败：{str(e)}，将训练新模型")

        texts = [event['text'] for event in self.historical_events]
        if not texts:
            raise ValueError("没有有效的文本数据用于训练")

        print(f"准备训练数据，共 {len(texts)} 条文本")
        sentences = [text.split() for text in texts]

        try:
            self.fasttext_model = FastText(
                sentences,
                min_count=min_count,
                vector_size=vector_size,
                window=window,
                sg=sg,
                epochs=epochs
            )
            print("FastText模型训练成功")

            # 如果指定了 model_path，则保存模型到磁盘
            if self.model_path:
                try:
                    self.fasttext_model.save(self.model_path)
                    print(f"模型已保存到 {self.model_path}")
                except Exception as e:
                    print(f"保存模型失败：{str(e)}")

            return self.fasttext_model
        except Exception as e:
            raise ValueError(f"训练FastText模型时出错：{str(e)}")

    def get_text_vector(self, text):
        """
        Get FastText vector for a text

        Args:
            text: Input text

        Returns:
            Vector representation of the text
        """
        if self.fasttext_model is None:
            raise ValueError("FastText model not trained yet!")

        # Split text into words and get vectors
        words = text.split()
        word_vectors = [self.fasttext_model.wv[word] for word in words if word in self.fasttext_model.wv]

        if not word_vectors:
            # Return zeros if no words found in the model vocabulary
            return np.zeros(self.fasttext_model.vector_size)

        # Average the word vectors to get text vector
        return np.mean(word_vectors, axis=0)

    def compute_similarity(self, new_event, historical_event):
        """
        Compute similarity between two events with time decay factor

        Args:
            new_event: Dictionary with new event data
            historical_event: Dictionary with historical event data

        Returns:
            Similarity score (higher means more similar)
        """
        # Get vectors
        new_vector = self.get_text_vector(new_event['text'])
        hist_vector = self.get_text_vector(historical_event['text'])

        # Compute cosine similarity
        vectors_reshaped = np.array([new_vector, hist_vector]).reshape(2, -1)
        cos_sim = cosine_similarity(vectors_reshaped)[0, 1]

        # Apply time decay factor
        time_diff = abs(new_event['timestamp'] - historical_event['timestamp']) / (24 * 3600)  # Convert to days
        time_decay = np.exp(-self.alpha * time_diff)

        # Final similarity with time decay
        similarity = cos_sim * time_decay

        return similarity

    def find_similar_events(self, new_event):
        """
        Find K most similar historical events

        Args:
            new_event: Dictionary with new event data

        Returns:
            List of K most similar events with similarity scores
        """
        similarities = []

        for hist_event in self.historical_events:
            sim_score = self.compute_similarity(new_event, hist_event)
            similarities.append((hist_event, sim_score))

        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top K
        return similarities[:self.k]

    def predict_root_cause(self, new_event):
        """
        Predict root cause for a new event based on similar historical events

        Args:
            new_event: Dictionary with new event data

        Returns:
            Predicted root cause type and explanation
        """
        similar_events = self.find_similar_events(new_event)

        if not similar_events:
            return None, "No similar historical events found"

        # Count occurrences of each label
        label_counts = {}
        for event, score in similar_events:
            label = event['label']
            if label not in label_counts:
                label_counts[label] = {'count': 0, 'score_sum': 0}
            label_counts[label]['count'] += 1
            label_counts[label]['score_sum'] += score

        # Find the most frequent label, weighted by similarity score
        predicted_label = max(label_counts.items(), key=lambda x: x[1]['score_sum'])[0]
        # 转换为故障类型
        predicted_type = self.fault_type_mapping.get(predicted_label, 'Unknown')

        # Create explanation
        explanation = f"Predicted root cause type: {predicted_type}\n\n"
        explanation += "Top similar historical events:\n"
        for i, (event, score) in enumerate(similar_events):
            event_type = self.fault_type_mapping.get(event['label'], 'Unknown')
            explanation += f"{i + 1}. fault{event['label']} ({event_type}) (similarity: {score:.4f})\n"
            if not event['data']['logs'].empty and 'Log' in event['data']['logs'].columns:
                top_logs = event['data']['logs']['Log'].dropna().head(2).tolist()
                for log in top_logs:
                    explanation += f"   - {log[:100]}...\n"

        return predicted_type, explanation

    def analyze_new_fault(self, log_path, trace_path, metric_path):
        """
        Analyze a new fault event

        Args:
            log_path: Path to log.csv
            trace_path: Path to trace.csv
            metric_path: Path to metric.csv

        Returns:
            Predicted root cause label and explanation
        """
        # Check if model is trained
        if self.fasttext_model is None:
            raise ValueError("FastText model must be trained before analysis!")

        # 添加调试信息
        print(f"\n正在读取文件：")
        print(f"log文件: {log_path}")
        print(f"trace文件: {trace_path}")
        print(f"metric文件: {metric_path}")

        try:
            # Extract event features
            event_data = self.extract_event_features(log_path, trace_path, metric_path)
            event_text = self.event_to_text(event_data)
            timestamp = self.extract_timestamp(event_data)

            # Create new event object
            new_event = {
                'text': event_text,
                'data': event_data,
                'timestamp': timestamp
            }

            # Predict root cause
            label, explanation = self.predict_root_cause(new_event)

            return label, explanation
        except Exception as e:
            print(f"分析故障时出错：{str(e)}")
            raise

    def evaluate(self, test_ratio=0.2, random_state=42):
        """
        Evaluate the RCA system using train-test split

        Args:
            test_ratio: Ratio of test data
            random_state: Random seed for reproducibility

        Returns:
            Evaluation metrics dictionary
        """
        if not self.historical_events:
            raise ValueError("No historical events loaded!")

        X = self.historical_events
        y = self.historical_labels

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_ratio, random_state=random_state, stratify=y
        )

        # 保存原始数据
        original_events = self.historical_events
        original_labels = self.historical_labels

        # 设置为训练数据
        self.historical_events = X_train
        self.historical_labels = y_train

        # 训练模型（仅在未训练时）
        self.train_fasttext_model()

        correct = 0
        predictions = []

        for i, test_event in enumerate(X_test):
            test_event_copy = test_event.copy()
            test_event_copy.pop('label', None)
            pred_label, _ = self.predict_root_cause(test_event_copy)
            true_label = y_test[i]
            predictions.append((pred_label, true_label))
            if pred_label == true_label:
                correct += 1

        accuracy = correct / len(X_test) if X_test else 0

        # 恢复原始数据
        self.historical_events = original_events
        self.historical_labels = original_labels

        return {
            'accuracy': accuracy,
            'predictions': predictions,
            'num_test_samples': len(X_test)
        }

    def analyze_error_patterns(self, new_log_path, new_trace_path, new_metric_path):
        """
        Analyze error patterns in logs

        Args:
            new_log_path: Path to log.csv
            new_trace_path: Path to trace.csv
            new_metric_path: Path to metric.csv

        Returns:
            Dictionary with error patterns
        """
        logs_df = pd.read_csv(new_log_path)

        # Extract error patterns
        error_patterns = {}

        # Count occurrences of error types
        if 'Log' in logs_df.columns:
            for log in logs_df['Log'].dropna():
                if 'ERROR' in log:
                    # Extract error message
                    error_match = re.search(r'ERROR\s+([^\[#]+)', log)
                    if error_match:
                        error_type = error_match.group(1).strip()
                        error_patterns[error_type] = error_patterns.get(error_type, 0) + 1

        # Sort by frequency
        sorted_errors = sorted(error_patterns.items(), key=lambda x: x[1], reverse=True)

        return {
            'top_errors': sorted_errors[:5],
            'total_errors': len(logs_df) if 'Log' in logs_df.columns else 0
        }

    def visualize_metrics(self, metric_path):
        """
        Visualize metrics data

        Args:
            metric_path: Path to metric.csv

        Returns:
            None (saves plot to file)
        """
        metrics_df = pd.read_csv(metric_path)
        metrics_df = metrics_df.dropna(how='all')

        if metrics_df.empty:
            print("No valid metrics data found")
            return

        plt.figure(figsize=(12, 8))

        if 'PodName' in metrics_df.columns and 'CpuUsageRate(%)' in metrics_df.columns:
            pods = metrics_df['PodName'].dropna().unique()

            for i, pod in enumerate(pods[:5]):
                pod_data = metrics_df[metrics_df['PodName'] == pod]

                plt.subplot(2, 1, 1)
                plt.plot(pod_data.index, pod_data['CpuUsageRate(%)'], label=pod)
                plt.title('CPU Usage Rate (%)')
                plt.legend()

                if 'MemoryUsageRate(%)' in metrics_df.columns:
                    plt.subplot(2, 1, 2)
                    plt.plot(pod_data.index, pod_data['MemoryUsageRate(%)'], label=pod)
                    plt.title('Memory Usage Rate (%)')
                    plt.legend()

        plt.tight_layout()
        plt.savefig('metrics_plot.png')  # 保存图像到文件
        print("Metrics plot saved to 'metrics_plot.png'")

def main():
    """
    主函数：用于手动输入故障编号进行根因分析
    """
    try:
        rca = RCASystem(model_path='fasttext_model.bin')
        print("正在加载历史故障数据...")
        try:
            rca.load_data()
        except ValueError as e:
            print(f"错误：{str(e)}")
            print("请确保：\n1. TrainTicket文件夹与fasttext.py在同一目录下\n2. TrainTicket文件夹中有fault1, fault2等故障文件夹\n3. 每个故障文件夹中都有完整的log.csv, trace.csv和metric.csv文件")
            return

        print("正在训练或加载FastText模型...")
        try:
            rca.train_fasttext_model()
        except ValueError as e:
            print(f"错误：{str(e)}")
            return

        while True:
            fault_num = input("\n请输入要分析的故障编号（输入'q'退出）: ")
            if fault_num.lower() == 'q':
                break
            try:
                fault_num = int(fault_num)
                fault_dir = f'fault_{fault_num}'
                log_path = f'./TrainTicket/{fault_dir}/log.csv'
                trace_path = f'./TrainTicket/{fault_dir}/trace.csv'
                metric_path = f'./TrainTicket/{fault_dir}/metric.csv'
                print(f"\n检查文件路径：\n故障目录: {fault_dir}\nlog文件: {log_path} - {'存在' if os.path.exists(log_path) else '不存在'}\ntrace文件: {trace_path} - {'存在' if os.path.exists(trace_path) else '不存在'}\nmetric文件: {metric_path} - {'存在' if os.path.exists(metric_path) else '不存在'}")
                if not all(os.path.exists(path) for path in [log_path, trace_path, metric_path]):
                    print(f"错误：故障{fault_num}的数据文件不完整，请检查文件是否存在")
                    continue
                print(f"\n正在分析故障{fault_num}...")
                fault_type, explanation = rca.analyze_new_fault(log_path, trace_path, metric_path)
                print("\n分析结果：\n" + "=" * 50 + f"\n预测的根因类型: {fault_type}\n\n详细解释：\n{explanation}\n" + "=" * 50)
                print("\n错误模式分析：")
                error_analysis = rca.analyze_error_patterns(log_path, trace_path, metric_path)
                for error_type, count in error_analysis['top_errors']:
                    print(f"- {error_type}: {count}次出现")
                print("\n正在生成指标可视化...")
                rca.visualize_metrics(metric_path)
            except ValueError:
                print("错误：请输入有效的数字")
            except Exception as e:
                print(f"分析过程中出现错误：{str(e)}")
    except Exception as e:
        print(f"系统初始化失败：{str(e)}")


if __name__ == "__main__":
    main()