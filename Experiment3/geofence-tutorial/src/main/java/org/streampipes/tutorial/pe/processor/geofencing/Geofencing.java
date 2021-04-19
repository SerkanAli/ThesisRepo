
package org.streampipes.tutorial.pe.processor.geofencing;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.util.Collector;

import org.streampipes.model.runtime.Event;

public class Geofencing implements FlatMapFunction<Event, Event> {

  @Override
  public void flatMap(Event in, Collector<Event> out) throws Exception {

    out.collect(in);
  }
}
