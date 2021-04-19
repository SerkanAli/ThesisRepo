package org.streampipes.tutorial.pe.processor.geofencing;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.util.Collector;
import org.streampipes.model.runtime.Event;

public class GeofencingProcessor implements FlatMapFunction<Event, Event> {

    private String latitudeFieldName;
    private String longitudeFieldName;

    private Float centerLatitude;
    private Float centerLongitude;

    private Integer radius;

    public GeofencingProcessor(String latitudeFieldName, String longitudeFieldName, Float centerLatitude, Float centerLongitude, Integer radius) {
        this.latitudeFieldName = latitudeFieldName;
        this.longitudeFieldName = longitudeFieldName;
        this.centerLatitude = centerLatitude;
        this.centerLongitude = centerLongitude;
        this.radius = radius;
    }

    @Override
    public void flatMap(Event in, Collector<Event> out) throws Exception {
        Float latitude = in.getFieldBySelector(latitudeFieldName).getAsPrimitive().getAsFloat();
        Float longitude = in.getFieldBySelector(longitudeFieldName).getAsPrimitive().getAsFloat();

        Float distance = distFrom(latitude, longitude, centerLatitude, centerLongitude);

        if (distance <= radius) {
            out.collect(in);
        }
    }

    public static Float distFrom(float lat1, float lng1, float lat2, float lng2) {
        double earthRadius = 6371000;
        double dLat = Math.toRadians(lat2-lat1);
        double dLng = Math.toRadians(lng2-lng1);
        double a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2)) *
                        Math.sin(dLng/2) * Math.sin(dLng/2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return (float) (earthRadius * c);
    }

}


