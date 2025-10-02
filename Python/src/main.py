import logging
from concurrent import futures

import grpc
import numpy as np
import torch

from agent import model
from generated import format_pb2, format_pb2_grpc
import config


def _state_to_numpy(state: format_pb2.State) -> np.ndarray:
    """Converts a gRPC State message to a NumPy array."""
    return np.array(
        [
            state.taskLength,
            state.taskMaxLatency,
            state.localCPU,
            state.localMIPSTerm,
            state.edgeCPUTerm,
            state.cloudCPUTerm,
            state.numberOfPes,
            state.fileSize,
            state.outputSize,
            state.containerSize,
            state.maxLatency,
        ],
        dtype=np.float32,
    )


class RLServer(format_pb2_grpc.UnaryServicer):
    def __init__(self) -> None:
        super().__init__()
        self.old_observation = None
        self.action = None
        self.agent = model.Agent(
            gamma=config.AGENT_GAMMA,
            epsilon=config.AGENT_EPSILON,
            batch_size=config.AGENT_BATCH_SIZE,
            n_actions=config.AGENT_N_ACTIONS,
            eps_end=config.AGENT_EPS_END,
            input_dims=config.AGENT_INPUT_DIMS,
            lr=config.AGENT_LR,
            max_mem_size=config.AGENT_MAX_MEM_SIZE,
            fc1_dims=config.DQN_FC1_DIMS,
            fc2_dims=config.DQN_FC2_DIMS,
        )
        self.scores = []

    def GetActionRL(self, request: format_pb2.State, context) -> format_pb2.Action:
        self.old_observation = _state_to_numpy(request)

        self.agent.Q_eval.eval()
        # The agent's choose_action method expects a numpy array
        self.action = self.agent.choose_action(observation=self.old_observation)
        self.agent.Q_eval.train()

        return format_pb2.Action(action=self.action)

    def TrainModelRL(self, request: format_pb2.TrainModelRequest, context) -> format_pb2.Response:
        if request.reward == 0.0:
            return format_pb2.Response(message="The model was not trained (reward is zero).")

        new_observation = _state_to_numpy(request.new_state)
        self.scores.append(request.reward)

        self.agent.store_transition(
            self.old_observation,
            action=self.action,
            reward=request.reward,
            state_=new_observation,
            done=request.is_done,
        )

        self.agent.learn()
        logging.info(f"Counter: {self.agent.counter}\tReward: {request.reward}")

        return format_pb2.Response(message="The model was trained.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    format_pb2_grpc.add_UnaryServicer_to_server(RLServer(), server)
    server.add_insecure_port(f"[::]:{config.SERVER_PORT}")
    server.start()
    logging.info(f"Server started, listening on port {config.SERVER_PORT}")
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("python_agent.log"),
            logging.StreamHandler()
        ]
    )
    serve()
