package my.groupId.main;

import org.streampipes.container.init.DeclarersSingleton;
import org.streampipes.container.standalone.init.StandaloneModelSubmitter;
import my.groupId.config.Config;
import my.groupId.pe.mypackagename.DataSource;

public class Init extends StandaloneModelSubmitter {

  public static void main(String[] args) throws Exception {
    DeclarersSingleton.getInstance()
            .add(new DataSource());

    new Init().init(Config.INSTANCE);

  }
}
