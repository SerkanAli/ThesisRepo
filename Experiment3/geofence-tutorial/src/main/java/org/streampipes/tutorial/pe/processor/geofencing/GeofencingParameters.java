package org.streampipes.tutorial.pe.processor.geofencing;

import org.streampipes.model.graph.DataProcessorInvocation;
import org.streampipes.wrapper.params.binding.EventProcessorBindingParams;


public class GeofencingParameters extends EventProcessorBindingParams {

  private String latitudeFieldName;
  private String longitudeFieldName;

  private Float centerLatitude;
  private Float centerLongitude;

  private Integer radius;

  public GeofencingParameters(DataProcessorInvocation graph, String latitudeFieldName, String longitudeFieldName,
                              Float centerLatitude, Float centerLongitude, Integer radius) {
    super(graph);
    this.latitudeFieldName = latitudeFieldName;
    this.longitudeFieldName = longitudeFieldName;
    this.centerLatitude = centerLatitude;
    this.centerLongitude = centerLongitude;
    this.radius = radius;
  }

  public String getLatitudeFieldName() {
    return latitudeFieldName;
  }

  public String getLongitudeFieldName() {
    return longitudeFieldName;
  }

  public Float getCenterLatitude() {
    return centerLatitude;
  }

  public Float getCenterLongitude() {
    return centerLongitude;
  }

  public Integer getRadius() {
    return radius;
  }
}

/*public class GeofencingParameters extends EventProcessorBindingParams {

  private String exampleText;

  public GeofencingParameters(DataProcessorInvocation graph, String exampleText) {
    super(graph);
    this.exampleText = exampleText;
  }

  public String getExampleText() {
    return exampleText;
  }

}
*/