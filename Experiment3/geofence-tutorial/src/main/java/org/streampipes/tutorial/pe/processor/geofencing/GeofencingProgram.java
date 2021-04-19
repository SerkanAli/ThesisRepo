package org.streampipes.tutorial.pe.processor.geofencing;

import org.streampipes.tutorial.config.Config;

import org.apache.flink.streaming.api.datastream.DataStream;
import org.streampipes.model.runtime.Event;
import org.streampipes.wrapper.flink.FlinkDataProcessorRuntime;
import org.streampipes.wrapper.flink.FlinkDeploymentConfig;

import java.io.Serializable;

public class GeofencingProgram extends
        FlinkDataProcessorRuntime<GeofencingParameters>
implements Serializable {

  private static final long serialVersionUID = 1L;

  public GeofencingProgram(GeofencingParameters params, boolean debug) {
    super(params, debug);
  }

  protected FlinkDeploymentConfig getDeploymentConfig() {
    return new FlinkDeploymentConfig(Config.JAR_FILE,
            Config.INSTANCE.getFlinkHost(), Config.INSTANCE.getFlinkPort());
  }

  protected DataStream<Event> getApplicationLogic(
        DataStream<Event>... messageStream) {

    return messageStream[0].flatMap(new GeofencingProcessor(params.getLatitudeFieldName(), params.getLongitudeFieldName(),
            params.getCenterLatitude(), params.getCenterLongitude(), params.getRadius()));

  }
}
