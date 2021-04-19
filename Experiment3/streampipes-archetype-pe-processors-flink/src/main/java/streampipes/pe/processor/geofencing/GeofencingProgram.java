package streampipes.pe.processor.geofencing;


import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.streampipes.model.runtime.Event;
import org.apache.streampipes.wrapper.flink.FlinkDataProcessorRuntime;
import org.apache.streampipes.wrapper.flink.FlinkDeploymentConfig;
import streampipes.config.Config;

import java.io.Serializable;

public class GeofencingProgram extends
        FlinkDataProcessorRuntime<GeofencingParameters>
implements Serializable {

  private static final long serialVersionUID = 1L;

  public GeofencingProgram(GeofencingParameters params, boolean debug) {
    super(params, debug);
  }

  @Override
  protected DataStream<Event> getApplicationLogic(DataStream<Event>... dataStreams) {
    return dataStreams[0].flatMap(new GeofencingProcessor(params.getLatitudeFieldName(), params.getLongitudeFieldName(),
            params.getCenterLatitude(), params.getCenterLongitude(), params.getRadius()));
  }

  protected FlinkDeploymentConfig getDeploymentConfig() {
    return new FlinkDeploymentConfig(Config.JAR_FILE,
            Config.INSTANCE.getFlinkHost(), Config.INSTANCE.getFlinkPort());
  }
}
