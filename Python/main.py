import grpc
from concurrent import futures
import format_pb2_grpc
import format_pb2
import logging
from neural_network import model
import numpy as np
import torch


class RLServer(format_pb2_grpc.UnaryServicer):
    def __init__(self) -> None:
        super().__init__()
        self.old_observation = None
        self.action = None
        self.agent = model.Agent(
            gamma=0.99,
            epsilon=0.15,
            batch_size=128,
            n_actions=4,
            eps_end=0.01,
            input_dims=[11],
            lr=3e-3,
        )
        self.scores, self.eps_history = [], []

    def GetActionRL(self, request, context):
        taskLength = request.taskLength
        taskMaxLatency = request.taskMaxLatency
        localCPU = request.localCPU
        localMIPSTerm = request.localMIPSTerm
        edgeCPUTerm = request.edgeCPUTerm
        cloudCPUTerm = request.cloudCPUTerm
        numberOfPes = request.numberOfPes
        fileSize = request.fileSize
        outputSize = request.outputSize
        containerSize = request.containerSize
        maxLatency = request.maxLatency

        self.old_observation = torch.tensor(
            [
                taskLength,
                taskMaxLatency,
                localCPU,
                localMIPSTerm,
                edgeCPUTerm,
                cloudCPUTerm,
                numberOfPes,
                fileSize,
                outputSize,
                containerSize,
                maxLatency,
            ],
            dtype=torch.float32,
        )

        self.agent.Q_eval.eval()
        self.action = self.agent.choose_action(observation=self.old_observation)

        self.agent.Q_eval.train()
        return format_pb2.Action(action=self.action)

    def TrainModelRL(self, request, context):
        new_observation = request.new_state
        reward = request.reward
        done = request.is_done

        if reward != 0.0:
            self.new_observation = np.array(
                [
                    new_observation.taskLength,
                    new_observation.taskMaxLatency,
                    new_observation.localCPU,
                    new_observation.localMIPSTerm,
                    new_observation.edgeCPUTerm,
                    new_observation.cloudCPUTerm,
                    new_observation.numberOfPes,
                    new_observation.fileSize,
                    new_observation.outputSize,
                    new_observation.contapfinerSize,
                    new_observation.maxLatency,
                ]
            )

            self.scores += [reward]
            self.agent.store_transition(
                self.old_observation,
                action=self.action,
                reward=reward,
                state_=self.new_observation,
                done=done,
            )

            # if random.random() > 0.4:
            self.agent.learn()
            print(f"Counter: {self.agent.counter}\tReward: {reward}")
            return format_pb2.Response(message="the model trained!")

        else:
            return format_pb2.Response(message="the model didn't trained!")


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    format_pb2_grpc.add_UnaryServicer_to_server(RLServer(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
