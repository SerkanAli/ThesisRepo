
package my.groupId.pe.mypackagename;

import org.streampipes.container.declarer.DataStreamDeclarer;
import org.streampipes.container.declarer.SemanticEventProducerDeclarer;
import org.streampipes.model.graph.DataSourceDescription;
import org.streampipes.sdk.builder.DataSourceBuilder;

import java.util.Arrays;
import java.util.List;


public class DataSource implements SemanticEventProducerDeclarer {

  public DataSourceDescription declareModel() {
    return DataSourceBuilder.create("my.groupId.mypackagename.source", "MySource " +
        "Source", "twitter example")
            .build();
  }

  public List<DataStreamDeclarer> getEventStreams() {
    return Arrays.asList(new MySourceStream());
  }
}