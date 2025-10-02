# Cloud-Edge Task Orchestration using Reinforcement Learning

This project implements a Reinforcement Learning (RL) based approach for dynamic task orchestration in a simulated cloud-edge computing environment.

## Project Description

The core of this project is to intelligently decide whether to process a given computational task on a resource-constrained edge device or to offload it to a more powerful cloud server. This decision-making process is handled by a Python-based RL agent that communicates with a Java-based cloud-edge simulation environment.

The simulation, built upon PureEdgeSim, generates tasks and simulates network conditions, device mobility, and resource availability. The RL agent, implemented in Python using a neural network, learns an optimal policy for task placement based on the state of the simulated environment.

Communication between the Java simulation and the Python RL agent is achieved through gRPC.

## Key Components

### 1. Java Simulation Environment (`CloudRL/`)

This component simulates the cloud-edge infrastructure.

-   **`CloudRL/src/main/java/pruebas/MultiLayerRLManager_python.java`**: This class acts as the manager within the simulation, interfacing with the Python RL agent to get decisions for task placement.
-   **`CloudRL/src/main/java/pruebas/RLClient.java`**: The gRPC client responsible for sending state information from the simulation to the Python server and receiving the chosen action.
-   **`CloudRL/src/main/java/output/`**: This directory contains the results and logs generated from the simulation runs, such as task execution times, energy consumption, and network usage.
-   **`CloudRL/src/main/java/pruebas/settings/`**: Contains configuration files for different simulation scenarios.

### 2. Python Reinforcement Learning Agent (`Python/`)

This component contains the "brain" of the orchestration system.

-   **`Python/main.py`**: The main entry point that runs a gRPC server. It waits for requests from the Java client, processes the environment state, and uses the neural network to select an action (i.e., where to execute the task).
-   **`Python/neural_network/model.py`**: Defines the neural network architecture used for the RL agent.
-   **`Python/protos/format.proto`**: The protobuf file that defines the structure of the gRPC messages exchanged between the Java client and the Python server.

## How It Works

1.  The Java simulation is started, configured by one of the scenarios in the `settings` directory.
2.  When a new task is generated, the `MultiLayerRLManager_python` is invoked.
3.  The `RLClient` sends the current system state (e.g., device battery, network latency, CPU load) to the Python RL agent via a gRPC call.
4.  The Python gRPC server in `main.py` receives the state and feeds it into the neural network model.
5.  The model outputs an action, which determines whether the task should be processed on the edge or in the cloud.
6.  This action is sent back to the Java client.
7.  The simulation environment executes the task according to the agent's decision and proceeds.
8.  Simulation results are logged in the `output` directory for analysis.
