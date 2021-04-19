package org.streampipes.tutorial.main;

import org.streampipes.container.init.DeclarersSingleton;
import org.streampipes.container.standalone.init.StandaloneModelSubmitter;

import org.streampipes.tutorial.config.Config;
import org.streampipes.tutorial.pe.processor.geofencing.GeofencingController;

import org.streampipes.dataformat.cbor.CborDataFormatFactory;
import org.streampipes.dataformat.fst.FstDataFormatFactory;
import org.streampipes.dataformat.json.JsonDataFormatFactory;
import org.streampipes.dataformat.smile.SmileDataFormatFactory;
import org.streampipes.messaging.jms.SpJmsProtocolFactory;
import org.streampipes.messaging.kafka.SpKafkaProtocolFactory;

public class Init extends StandaloneModelSubmitter {

  public static void main(String[] args) throws Exception {
    DeclarersSingleton.getInstance()
            .add(new GeofencingController());

    /*DeclarersSingleton.getInstance().registerDataFormats(new JsonDataFormatFactory(),
            new CborDataFormatFactory(),
            new SmileDataFormatFactory(),
            new FstDataFormatFactory());

    DeclarersSingleton.getInstance().registerProtocols(new SpKafkaProtocolFactory(),
            new SpJmsProtocolFactory());*/

    new Init().init(Config.INSTANCE);

  }


}
