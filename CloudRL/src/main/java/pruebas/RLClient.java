package pruebas;

import io.grpc.*;
import unary.Format;
import unary.UnaryGrpc;

import java.text.Normalizer;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
import java.util.logging.Logger;

class RLClient {
    private final Logger logger = Logger.getLogger(RLClient.class.getName());

    private final UnaryGrpc.UnaryBlockingStub blockingStub;

    RLClient(Channel channel) {
        this.blockingStub = UnaryGrpc.newBlockingStub(channel);
    }

    public int getActionFromPython(Map<String, Double> values) {
//        logger.info("Will try to an action");
        Format.State state = setState(values);
        // numberOfPes
        // fileSize
        // outputSize
        // containerSize
        // maxLatency

        Format.Action response;
        try {
            response = blockingStub.getActionRL(state);
        } catch (StatusRuntimeException e) {
            logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
            return -1;
        }
//        logger.info("Action Performed: " + response.getAction());

        return response.getAction();
    }

    public void makePythonModelLearn(Map<String, Double> new_observation, double reward, boolean done) {
//        logger.info("Python Model will try to learn now");
        Format.State new_state = setState(new_observation);

        Format.TrainModelRequest request = Format.TrainModelRequest.newBuilder()
                .setNewState(new_state)
                .setReward(reward)
                .setIsDone(done)
                .build();

        Format.Response response;
        try {
            response = blockingStub.trainModelRL(request);
        } catch (StatusRuntimeException e) {
            logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
            return;
        }

//        logger.info(response.getMessage());
    }

    private Format.State setState(Map<String, Double> observation) {
        return Format.State.newBuilder().
                setCloudCPUTerm(observation.get("CloudCPUTerm")).
                setLocalCPU(observation.get("LocalCPU")).
                setEdgeCPUTerm(observation.get("EdgeCPUTerm")).
                setLocalMIPSTerm(observation.get("LocalMIPSTerm")).
                setTaskLength(observation.get("TaskLength")).
                setTaskMaxLatency(observation.get("TaskMaxLength")).
                setNumberOfPes(observation.get("numberOfPes")).
                setFileSize(observation.get("fileSize")).
                setOutputSize(observation.get("outputSize")).
                setContainerSize(observation.get("containerSize")).
                setMaxLatency(observation.get("maxLatency")).
                build();
    }

    public static void main(String[] args) throws InterruptedException {
        String user = "world";
        // Access a service running on the local machine on port 50051
        String target = "localhost:50051";

        ManagedChannel channel = Grpc.newChannelBuilder(target, InsecureChannelCredentials.create())
                .build();

        Map<String, Double> state = new HashMap<>();
        state.put("TaskLength", 0.0);
        state.put("TaskMaxLength", 0.0);
        state.put("LocalMIPSTerm", 0.0);
        state.put("EdgeCPUTerm", 0.0);
        state.put("LocalCPU", 0.0);
        state.put("CloudCPUTerm", 0.0);

        Map<String, Double> new_state = new HashMap<>();
        new_state.put("TaskLength", 0.0);
        new_state.put("TaskMaxLength", 0.0);
        new_state.put("LocalMIPSTerm", 0.0);
        new_state.put("EdgeCPUTerm", 0.0);
        new_state.put("LocalCPU", 0.0);
        new_state.put("CloudCPUTerm", 0.0);

        try {
            RLClient client = new RLClient(channel);
            client.getActionFromPython(state);
            client.makePythonModelLearn(new_state, 0.0, false);
            client.makePythonModelLearn(new_state, 0.0, false);
        } finally {
            // ManagedChannels use resources like threads and TCP connections. To prevent leaking these
            // resources the channel should be shut down when it will no longer be used. If it may be used
            // again leave it running.
            channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
        }
    }
}