
package my.groupId.pe.mypackagename;

import com.google.gson.JsonObject;
import org.streampipes.messaging.kafka.SpKafkaProducer;
import org.streampipes.model.SpDataStream;
import org.streampipes.model.graph.DataSourceDescription;
import org.streampipes.sdk.builder.DataStreamBuilder;
import org.streampipes.sdk.helpers.EpProperties;
import org.streampipes.sdk.helpers.Formats;
import org.streampipes.sdk.helpers.Labels;
import org.streampipes.sdk.helpers.Protocols;
import org.streampipes.sources.AbstractAdapterIncludedStream;
import org.streampipes.vocabulary.Geo;

import java.util.Random;


public class MySourceStream extends AbstractAdapterIncludedStream {

  @Override
  public SpDataStream declareModel(DataSourceDescription sep) {
    return DataStreamBuilder.create("my.groupId-mypackagename", "MySource", "")
            .property(EpProperties.timestampProperty("timestamp"))
            .property(EpProperties.stringEp(Labels.from("some-example-text", "Example Text", "This provides some example english text for the ELG service"), "exampleenglishtext", "http://my.company/plateNumber"))
            .format(Formats.jsonFormat())
            .protocol(Protocols.kafka("localhost", 9094, "org.streampipes.tutorial.vehicle"))
            .build();
  }

  @Override
  public void executeStream() {
    SpKafkaProducer producer = new SpKafkaProducer("localhost:9094", "org.streampipes.tutorial.vehicle");
    Random random = new Random();
    Runnable runnable = new Runnable() {
      @Override
      public void run() {
        for (;;) {
          JsonObject jsonObject = new JsonObject();
          jsonObject.addProperty("timestamp", System.currentTimeMillis());
          jsonObject.addProperty("exampleenglishtext", "In this example");

          producer.publish(jsonObject.toString());

          try {
            Thread.sleep(10000); //10 seconds
            System.out.println("One more Time!");
          } catch (InterruptedException e) {
            e.printStackTrace();
          }

        }
      }
    };

    new Thread(runnable).start();
  }
}
