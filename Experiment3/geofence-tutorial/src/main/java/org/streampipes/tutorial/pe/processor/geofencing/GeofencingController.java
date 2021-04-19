package org.streampipes.tutorial.pe.processor.geofencing;

import org.streampipes.model.schema.PropertyScope;
import org.streampipes.tutorial.config.Config;

import org.streampipes.model.DataProcessorType;
import org.streampipes.model.graph.DataProcessorDescription;
import org.streampipes.model.graph.DataProcessorInvocation;
import org.streampipes.sdk.builder.ProcessingElementBuilder;
import org.streampipes.sdk.builder.StreamRequirementsBuilder;
import org.streampipes.sdk.extractor.ProcessingElementParameterExtractor;
import org.streampipes.sdk.helpers.EpRequirements;
import org.streampipes.sdk.helpers.Labels;
import org.streampipes.sdk.helpers.OutputStrategies;
import org.streampipes.sdk.helpers.SupportedFormats;
import org.streampipes.sdk.helpers.SupportedProtocols;
import org.streampipes.sdk.helpers.*;
import org.streampipes.sdk.utils.Assets;
import org.streampipes.vocabulary.Geo;
import org.streampipes.wrapper.flink.FlinkDataProcessorDeclarer;
import org.streampipes.wrapper.flink.FlinkDataProcessorRuntime;

public class GeofencingController extends
				FlinkDataProcessorDeclarer<GeofencingParameters> {

	private static final String EXAMPLE_KEY = "example-key";

	@Override
	public DataProcessorDescription declareModel() {
		return ProcessingElementBuilder.create("org.streampipes.tutorial.geofencing", "Geofencing", "A simple geofencing data processor " +
				"using the Apache Flink wrapper")
				.requiredStream(StreamRequirementsBuilder
					.create()
					.requiredPropertyWithUnaryMapping(EpRequirements.domainPropertyReq(Geo.lat),
						Labels.from("latitude-field", "Latitude", "The event " +
								"property containing the latitude value"), PropertyScope.MEASUREMENT_PROPERTY)
				.requiredPropertyWithUnaryMapping(EpRequirements.domainPropertyReq(Geo.lng),
						Labels.from("longitude-field", "Longitude", "The event " +
								"property containing the longitude value"), PropertyScope.MEASUREMENT_PROPERTY)
				.build())
				.requiredIntegerParameter("radius", "Geofence Size", "The size of the circular geofence in meters.", 0, 1000, 1)
				.requiredOntologyConcept(Labels.from("location", "Geofence Center", "Provide the coordinate of the " +
						"geofence center"), OntologyProperties.mandatory(Geo.lat), OntologyProperties.mandatory(Geo.lng))
				.supportedProtocols(SupportedProtocols.kafka())
				.supportedFormats(SupportedFormats.jsonFormat())
				.outputStrategy(OutputStrategies.keep())
				.build();






		/*return ProcessingElementBuilder.create("org.streampipes.tutorial.pe.processor.geofencing")
        		.withAssets(Assets.DOCUMENTATION, Assets.ICON)
						.withLocales(Locales.EN)
						.category(DataProcessorType.ENRICH)
						.requiredStream(StreamRequirementsBuilder
							.create()
							.requiredProperty(EpRequirements.anyProperty())
							.build())
						.supportedFormats(SupportedFormats.jsonFormat())
						.supportedProtocols(SupportedProtocols.kafka())
						.outputStrategy(OutputStrategies.keep())
						.requiredTextParameter(Labels.withId(EXAMPLE_KEY))
						.build();
						*/

	}

	@Override
	public FlinkDataProcessorRuntime<GeofencingParameters> getRuntime(DataProcessorInvocation
				graph, ProcessingElementParameterExtractor extractor) {

		String exampleString = extractor.singleValueParameter(EXAMPLE_KEY, String.class);
		String latitudeFieldName = extractor.mappingPropertyValue("latitude-field");
		String longitudeFieldName = extractor.mappingPropertyValue("longitude-field");
		Float centerLatitude = extractor.supportedOntologyPropertyValue("location", Geo.lat, Float.class);
		Float centerLongitude = extractor.supportedOntologyPropertyValue("location", Geo.lng, Float.class);
		Integer radius = extractor.singleValueParameter("radius", Integer.class);

		GeofencingParameters params = new GeofencingParameters(graph, latitudeFieldName,
				longitudeFieldName, centerLatitude, centerLongitude, radius);

		return new GeofencingProgram(params, true);
	}

}
