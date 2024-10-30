The [TrainTicket](https://github.com/FudanSELab/train-ticket) project uses a microservices architecture based on Spring Cloud, with detailed components as follows:

### 1. **Architecture Overview**
   TrainTicket is structured with over 30 independent microservices, each handling specific functions, enabling separate development, deployment, and maintenance. This setup promotes scalability and fault tolerance.

### 2. **Service Layering**
   Key service layers in the system include:
   - **User Services**: Handling user management, authentication, and identity verification.
   - **Order Services**: Responsible for creating, querying, and managing ticket orders.
   - **Payment Services**: Manages payment processing for orders, handling both transactions and refunds.
   - **Ticket Management Services**: Includes seat allocation and reservation management, ensuring orderly ticket distribution.
   - **Notification Services**: Pushes status updates and notifications regarding orders and ticket availability.

### 3. **Core Components**
   - **Spring Boot and Spring Cloud**: Spring Boot serves as the base framework for each microservice, while Spring Cloud provides the distributed system support essential in microservices architecture, such as service registration, discovery, load balancing, and configuration management.
   - **Service Discovery & Registration (Eureka)**: Eureka Server manages service registration and discovery, allowing dynamic service connections within the cluster and enhancing flexibility and availability.
   - **API Gateway (Zuul)**: Zuul acts as the entry point for user requests, routing them to backend microservices. It enables authentication, routing control, and load balancing, improving security and simplifying frontend development.
   - **Load Balancing (Ribbon)**: The Ribbon client-side load balancer distributes requests, dynamically selecting the optimal instance for balanced load distribution to prevent any single point from overloading.

### 4. **Fault Tolerance & Recovery**
   - **Circuit Breaker & Fallback (Hystrix)**: Hystrix manages circuit breaking and fallback responses under high load or during service exceptions. When a service fails, Hystrix quickly breaks the circuit and returns default values or fallback options to prevent issues from propagating.
   - **Rate Limiting**: Through Hystrix’s thread pool isolation, the system prevents overload by limiting sudden influxes of requests, protecting resources from overuse.

### 5. **Data Management and Storage**
   - **Distributed Databases**: Each service has its own database, reducing data coupling. MySQL and MongoDB are used to store structured and unstructured data, ensuring high availability and scalability through partitioning and clustering.
   - **Data Consistency**: Distributed transactions and message queues (like Kafka or RabbitMQ) ensure asynchronous updates and synchronization, maintaining consistency across distributed services.

### 6. **Monitoring and Logging**
   - **Centralized Monitoring**: Integrated with Prometheus and Grafana to track real-time system health and performance metrics, allowing prompt fault detection and resolution.
   - **Log Aggregation**: ELK (Elasticsearch, Logstash, Kibana) or similar solutions are used to collect logs across services, simplifying fault diagnosis and event tracking.

### 7. **Message Queue Support**
   Kafka or RabbitMQ is used as the message queue to enable asynchronous events and notifications across services. This reduces direct dependencies between modules and improves the system’s concurrency handling.

### 8. **High Concurrency and High Availability Design**
   - **Cache Layer**: Caching with Redis or other middleware for high-frequency data to reduce database load and enhance response times.
   - **Cluster Deployment**: Docker and Kubernetes enable automated deployment and clustered management, ensuring smooth scalability and fault isolation.

These design choices and components give TrainTicket strong flexibility, scalability, and resilience, capable of handling high traffic loads while efficiently managing service failures and peak loads.

### 9.The detail of Container Image

| Service Name                 | Base Image          | Timezone      | Memory Limit | Expose Port | JAR File                                  |
| ---------------------------- | ------------------- | ------------- | ------------ | ----------- | ----------------------------------------- |
| ts-admin-basic-info-service  | java:8-jre          | Asia/Shanghai | 200m         | 18767       | /app/ts-admin-basic-info-service-1.0.jar  |
| ts-admin-order-service       | java:8-jre          | Asia/Shanghai | 200m         | 16112       | /app/ts-admin-order-service-1.0.jar       |
| ts-admin-route-service       | java:8-jre          | Asia/Shanghai | 200m         | 16113       | /app/ts-admin-route-service-1.0.jar       |
| ts-admin-travel-service      | java:8-jre          | Asia/Shanghai | 200m         | 16114       | /app/ts-admin-travel-service-1.0.jar      |
| ts-admin-user-service        | java:8-jre          | Asia/Shanghai | 200m         | 16115       | /app/ts-admin-user-service-1.0.jar        |
| ts-assurance-service         | java:8-jre          | Asia/Shanghai | 200m         | 18888       | /app/ts-assurance-service-1.0.jar         |
| ts-auth-service              | java:8-jre          | Asia/Shanghai | 200m         | 16116       | /app/ts-auth-service-1.0.jar              |
| ts-avatar-service            | python:3            | Asia/Shanghai | None         | 17001       | gunicorn-Python                           |
| ts-basic-service             | java:8-jre          | Asia/Shanghai | 200m         | 15680       | /app/ts-basic-service-1.0.jar             |
| ts-cancel-service            | java:8-jre          | Asia/Shanghai | 200m         | 18885       | /app/ts-cancel-service-1.0.jar            |
| ts-common                    | None                | None          | None         | None        | None                                      |
| ts-config-service            | java:8-jre          | Asia/Shanghai | 200m         | 15679       | /app/ts-config-service-1.0.jar            |
| ts-consign-price-service     | java:8-jre          | Asia/Shanghai | 200m         | 16110       | /app/ts-consign-price-service-1.0.jar     |
| ts-consign-service           | java:8-jre          | Asia/Shanghai | 200m         | 16109       | /app/ts-consign-service-1.0.jar           |
| ts-contacts-service          | java:8-jre          | Asia/Shanghai | 200m         | 12347       | /app/ts-contacts-service-1.0.jar          |
| ts-delivery-service          | java:8-jre          | Asia/Shanghai | 200m         | 18880       | /app/ts-delivery-service-1.0.jar          |
| ts-execute-service           | java:8-jre          | Asia/Shanghai | 200m         | 12386       | /app/ts-execute-service-1.0.jar           |
| ts-food-delivery-service     | java:8-jre          | Asia/Shanghai | 200m         | 18957       | /app/ts-food-delivery-service-1.0.jar     |
| ts-food-service              | java:8-jre          | Asia/Shanghai | 200m         | 18856       | /app/ts-food-service-1.0.jar              |
| ts-gateway-service           | java:8-jre          | Asia/Shanghai | 1024m        | 18888       | /app/ts-gateway-service-1.0.jar           |
| ts-inside-payment-service    | java:8-jre          | Asia/Shanghai | 200m         | 18673       | /app/ts-inside-payment-service-1.0.jar    |
| ts-news-service              | mrrm/web.go         | None          | None         | 12862       | Go                                        |
| ts-notification-service      | java:8-jre          | Asia/Shanghai | 200m         | 16117       | /app/ts-notification-service-1.0.jar      |
| ts-order-other-service       | java:8-jre          | Asia/Shanghai | 200m         | 12032       | /app/ts-order-other-service-1.0.jar       |
| ts-order-service             | java:8-jre          | Asia/Shanghai | 200m         | 12031       | /app/ts-order-service-1.0.jar             |
| ts-payment-service           | java:8-jre          | Asia/Shanghai | 200m         | 19001       | /app/ts-payment-service-1.0.jar           |
| ts-preserve-other-service    | java:8-jre          | Asia/Shanghai | 200m         | 14569       | /app/ts-preserve-other-service-1.0.jar    |
| ts-preserve-service          | java:8-jre          | Asia/Shanghai | 200m         | 14568       | /app/ts-preserve-service-1.0.jar          |
| ts-price-service             | java:8-jre          | Asia/Shanghai | 200m         | 16579       | /app/ts-price-service-1.0.jar             |
| ts-rebook-service            | java:8-jre          | Asia/Shanghai | 200m         | 18886       | /app/ts-rebook-service-1.0.jar            |
| ts-route-plan-service        | java:8-jre          | Asia/Shanghai | 200m         | 12389       | /app/ts-route-plan-service-1.0.jar        |
| ts-route-service             | java:8-jre          | Asia/Shanghai | 200m         | 12390       | /app/ts-route-service-1.0.jar             |
| ts-seat-service              | java:8-jre          | Asia/Shanghai | 200m         | 18001       | /app/ts-seat-service-1.0.jar              |
| ts-security-service          | java:8-jre          | Asia/Shanghai | 200m         | 11188       | /app/ts-security-service-1.0.jar          |
| ts-station-food-service      | java:8-jre          | Asia/Shanghai | 200m         | 18855       | /app/ts-station-food-service-1.0.jar      |
| ts-station-service           | java:8-jre          | Asia/Shanghai | 200m         | 12345       | /app/ts-station-service-1.0.jar           |
| ts-ticket-office-service     | node                | Asia/Shanghai | None         | 16108       | Node.js                                   |
| ts-train-food-service        | java:8-jre          | Asia/Shanghai | 200m         | 19999       | /app/ts-train-food-service-1.0.jar        |
| ts-train-service             | java:8-jre          | Asia/Shanghai | 200m         | 14567       | /app/ts-train-service-1.0.jar             |
| ts-travel-plan-service       | java:8-jre          | Asia/Shanghai | 200m         | 14322       | /app/ts-travel-plan-service-1.0.jar       |
| ts-travel-service            | java:8-jre          | Asia/Shanghai | 200m         | 12346       | /app/ts-travel-service-1.0.jar            |
| ts-travel2-service           | java:8-jre          | Asia/Shanghai | 200m         | 16346       | /app/ts-travel2-service-1.0.jar           |
| ts-ui-dashboard              | openresty/openresty | Asia/Shanghai | None         | None        | Nginx                                     |
| ts-user-service              | java:8-jre          | Asia/Shanghai | 200m         | 12346       | /app/ts-user-service-1.0.jar              |
| ts-verification-code-service | java:8-jre          | Asia/Shanghai | 200m         | 15678       | /app/ts-verification-code-service-1.0.jar |
| ts-voucher-service           | python:3            | Asia/Shanghai | None         | 16101       | Nginx                                     |
| ts-wait-order-service        | java:8-jre          | Asia/Shanghai | 200m         | 19999       | /app/ts-wait-order-service-1.0.jar        |