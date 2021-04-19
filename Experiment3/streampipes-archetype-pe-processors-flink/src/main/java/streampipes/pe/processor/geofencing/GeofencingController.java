package streampipes.pe.processor.geofencing;

import org.apache.streampipes.model.schema.PropertyScope;

import org.apache.streampipes.model.DataProcessorType;
import org.apache.streampipes.model.graph.DataProcessorDescription;
import org.apache.streampipes.model.graph.DataProcessorInvocation;
import org.apache.streampipes.sdk.builder.ProcessingElementBuilder;
import org.apache.streampipes.sdk.builder.StreamRequirementsBuilder;
import org.apache.streampipes.sdk.extractor.ProcessingElementParameterExtractor;
import org.apache.streampipes.sdk.helpers.EpRequirements;
import org.apache.streampipes.sdk.helpers.Labels;
import org.apache.streampipes.sdk.helpers.OutputStrategies;
import org.apache.streampipes.sdk.helpers.SupportedFormats;
import org.apache.streampipes.sdk.helpers.SupportedProtocols;
import org.apache.streampipes.sdk.helpers.*;
import org.apache.streampipes.sdk.utils.Assets;
import org.apache.streampipes.vocabulary.Geo;
import org.apache.streampipes.wrapper.flink.FlinkDataProcessorDeclarer;
import org.apache.streampipes.wrapper.flink.FlinkDataProcessorRuntime;

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
