package org.streampipes.tutorial.config;

import org.streampipes.config.SpConfig;
import org.streampipes.container.model.PeConfig;

public enum Config implements PeConfig {

  INSTANCE;

  private SpConfig config;
  public static final String JAR_FILE = "./streampipes-processing-element-container.jar";

  private final static String SERVICE_ID = "pe/org.streampipes.tutorial";


  Config() {
    config = SpConfig.getSpConfig(SERVICE_ID);

    config.register(ConfigKeys.HOST, "geofence-tutorial", "Hostname for the pe mixed flink component");
    config.register(ConfigKeys.PORT, 8090, "Port for the pe mixed flink component");
    config.register(ConfigKeys.FLINK_HOST, "jobmanager", "Host for the flink cluster");
    config.register(ConfigKeys.FLINK_PORT, 6123, "Port for the flink cluster");
    config.register(ConfigKeys.ICON_HOST, "backend", "Hostname for the icon host");
    config.register(ConfigKeys.ICON_PORT, 80, "Port for the icons in nginx");

    config.register(ConfigKeys.DEBUG, false, "When set to true programs are not deployed to cluster, but executed locally");

    config.register(ConfigKeys.SERVICE_NAME, "geofencing", "The name of the service");

  }

  @Override
  public String getHost() {
    return config.getString(ConfigKeys.HOST);
  }

  @Override
  public int getPort() {
    return config.getInteger(ConfigKeys.PORT);
  }

  public String getFlinkHost() {
    return config.getString(ConfigKeys.FLINK_HOST);
  }

  public int getFlinkPort() {
    return config.getInteger(ConfigKeys.FLINK_PORT);
  }

  public static final String iconBaseUrl = "http://" + Config.INSTANCE.getIconHost() + ":" +
          Config.INSTANCE.getIconPort() + "/assets/img/pe_icons";

  public static final String getIconUrl(String pictureName) {
    return iconBaseUrl + "/" + pictureName + ".png";
  }

  public String getIconHost() {
    return config.getString(ConfigKeys.ICON_HOST);
  }

  public int getIconPort() {
    return config.getInteger(ConfigKeys.ICON_PORT);
  }

  public boolean getDebug() {
    return config.getBoolean(ConfigKeys.DEBUG);
  }

  @Override
  public String getId() {
    return SERVICE_ID;
  }

  @Override
  public String getName() {
    return config.getString(ConfigKeys.SERVICE_NAME);
  }

}
