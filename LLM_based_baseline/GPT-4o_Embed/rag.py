import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from tooluse import *
import re
from dotenv import load_dotenv
from csv2md import remove_suffix

load_dotenv()
llm = ChatOpenAI(model="gpt-4o")
markdown_path = "rag_knowledge.md"
loader = UnstructuredMarkdownLoader(markdown_path)

docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(model="text-embedding-ada-002"))

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


if __name__ == "__main__":
    fault_time = read_txt_as_json()["inject_time"]
    fault_pod_suffix = read_txt_as_json()["inject_pod"]
    fault_pod = remove_suffix(remove_suffix(fault_pod_suffix))

    print(rag_chain.invoke("""You are an operations engineer proficient in root cause analysis of cloud events. 
                           Existing fault types include return errors, exceptions, network delay, and CPU contention. 
                           The current cloud system experienced a failure at """ + fault_time + ". The current " + fault_pod + """ service is affected.You are responsible for predicting the root cause based on existing data which includes logs, metrics, and traces. 
                           Please provide the root cause without exceeding the four failure types in the current system.
    
        •	Logs: [""" + partdata("log.csv") +"""]
        •	Metrics: [""" + partdata("metric.csv") +"""]
        •	Trace: [""" + partdata("trace.csv") +"""]
    
        """))