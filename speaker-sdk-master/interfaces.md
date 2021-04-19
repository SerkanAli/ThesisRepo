# Protocol Documentation
<a name="top"></a>

# Table of Contents

##  [speaker.proto](#speaker.proto)
### Services
 - [DialogueManager](#speaker.beta2.DialogueManager)
 - [SpeechRecognition](#speaker.beta2.SpeechRecognition)
 - [TextToSpeech](#speaker.beta2.TextToSpeech)
 - [VoiceAssistant](#speaker.beta2.VoiceAssistant)

### Messages
  - [AssistantConfig](#speaker.beta2.AssistantConfig)
  - [AssistantRequest](#speaker.beta2.AssistantRequest)
  - [AssistantResponse](#speaker.beta2.AssistantResponse)
  - [AudioFormat](#speaker.beta2.AudioFormat)
  - [DialogueRequest](#speaker.beta2.DialogueRequest)
  - [DialogueResponse](#speaker.beta2.DialogueResponse)
  - [SpeechRecognitionRequest](#speaker.beta2.SpeechRecognitionRequest)
  - [SpeechRecognitionRequest.Config](#speaker.beta2.SpeechRecognitionRequest.Config)
  - [SynthesizedSpeech](#speaker.beta2.SynthesizedSpeech)
  - [Transcript](#speaker.beta2.Transcript)
  - [Transcript.WordAlignment](#speaker.beta2.Transcript.WordAlignment)
  - [TtsRequest](#speaker.beta2.TtsRequest)

### Enumerations
  - [AssistantResponse.FollowUp](#speaker.beta2.AssistantResponse.FollowUp)
  - [AudioFormat.Encoding](#speaker.beta2.AudioFormat.Encoding)

- [Scalar Value Types](#scalar-value-types)



<a name="speaker.proto"></a>
<p align="right"><a href="#top">Top</a></p>

# speaker.proto


## Services

<a name="speaker.beta2.DialogueManager"></a>

### DialogueManager
This service handles incoming textual queries from the user or possibly
other events which may be triggered by some devices.

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| handle | [DialogueRequest](#speaker.beta2.DialogueRequest) | [DialogueResponse](#speaker.beta2.DialogueResponse) | Predict a response to the user input. |


<a name="speaker.beta2.SpeechRecognition"></a>

### SpeechRecognition
This service provides an interface for recognizing and transcribing speech
which has been recorded from the user.

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| transcribe | [SpeechRecognitionRequest](#speaker.beta2.SpeechRecognitionRequest) stream | [Transcript](#speaker.beta2.Transcript) stream | Transcribe the passed audio stream |


<a name="speaker.beta2.TextToSpeech"></a>

### TextToSpeech
This service synthesizes speech from a given text.

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| synthesize | [TtsRequest](#speaker.beta2.TtsRequest) | [SynthesizedSpeech](#speaker.beta2.SynthesizedSpeech) stream | Synthesize the given text as natural language |


<a name="speaker.beta2.VoiceAssistant"></a>

### VoiceAssistant
This is the voice assistant service which provides a single interface to conveniently access all
the other services during a conversation with the user. It bundles all three regular calls of a
voice interaction, to the speech recognizer, the dialogue manager and the speech synthesizer,
into one call.

Each call represents a single turn in the conversation between the user and the voice assistant
and consists of one or more streamed requests and responses between client and server.

#### Examples

This is an example for one turn using the full voice assistant, i.e. sending audio in and
receiving audio back:
* [IN] AssistantRequest.config
* [IN] AssistantRequest.audio_in
* [IN] AssistantRequest.audio_in
* [OUT] AssistantResponse.transcript
* [IN] AssistantRequest.audio_in
* [IN] AssistantRequest.audio_in
* [OUT] AssistantResponse.transcript
* [OUT] AssistantResponse.response
* [OUT] AssistantResponse.events
* [OUT] AssistantResponse.speech
* [OUT] AssistantResponse.speech
* [OUT] AssistantResponse.speech

Also a chatbot behaviour can be configured if the `AssistantConfig.text_query` field is set and
no `audio_out` configuration is provided:

* [IN] AssistantRequest.config
* [OUT] AssistantResponse.response
* [OUT] AssistantResponse.events

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| assist | [AssistantRequest](#speaker.beta2.AssistantRequest) stream | [AssistantResponse](#speaker.beta2.AssistantResponse) stream | This is a convenience function for interacting with the speech assistant. |

 <!-- end services -->

## Messages

<a name="speaker.beta2.AssistantConfig"></a>

### AssistantConfig
The audio configuration and internal state of the dialogue manager.

**Note:** Only one of the fields `audio_in` or `text_query` may be set at a time.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  | API key which selects the components to be used (e.g. German speech recognizer, dialogue manager for providing horoscopes and a female German speech synthesizer) |
| audio_in | [AudioFormat](#speaker.beta2.AudioFormat) |  | Configuration of incoming audio |
| text_query | [string](#string) |  | textual query from the user; if a query is provided here no further messages will be processed but this query is directly passed to the dialogue manager. |
| audio_out | [AudioFormat](#speaker.beta2.AudioFormat) |  | Desired configuration of the outgoing audio. |
| tracker | [bytes](#bytes) |  | Dialogue state (see same field in `DialogueRequest`) |
| debug | [bool](#bool) |  | True, if debug information for this request should also be returned |






<a name="speaker.beta2.AssistantRequest"></a>

### AssistantRequest
The top-level message which is sent as a stream from the client to the
server.

**Note:** Only one of the fields `config` or `audio_in` may be set at a time.
The first message has to contain the `config` field and all subsequent
messages have to contain the `audio_in` field.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| config | [AssistantConfig](#speaker.beta2.AssistantConfig) |  | The assistant's configuration for this request |
| audio_in | [bytes](#bytes) |  | Audio recording of user's query |






<a name="speaker.beta2.AssistantResponse"></a>

### AssistantResponse
The top-level message which is returned by the server.
One or more of these messages are sent to the client as a response, although only individual
fields may be set.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| speech | [bytes](#bytes) |  | Synthesized reponse of the assistant |
| reply | [string](#string) |  | Textual reply of the assistant |
| transcript | [string](#string) |  | Transcription of the user from the recording |
| stop_recording | [bool](#bool) |  | True, if the client should stop sending audio chunks since the speech recognizer has determined that the user's utterance has finished |
| events | [google.protobuf.Struct](#google.protobuf.Struct) | repeated | A list of client-specific events triggered by the request (see same field in message `DialogueResponse`) |
| follow_up | [AssistantResponse.FollowUp](#speaker.beta2.AssistantResponse.FollowUp) |  | Flag indicating whether the assistant expects further input from the user |
| tracker | [bytes](#bytes) |  | Dialogue state after processing the current request |
| html | [string](#string) |  | A visual response in form of a HTML5 document |
| debug_info | [google.protobuf.Struct](#google.protobuf.Struct) |  | Debug information needed to reconstruct the request in case of an error. |






<a name="speaker.beta2.AudioFormat"></a>

### AudioFormat
The audio format that is used for the transmitted audio.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| encoding | [AudioFormat.Encoding](#speaker.beta2.AudioFormat.Encoding) |  | Desired or provided audio encoding |
| samplerate | [uint32](#uint32) |  | If the encoding is PCM16 this field has to be set to the samplerate used to record the signal; otherwise this field will be ignored |






<a name="speaker.beta2.DialogueRequest"></a>

### DialogueRequest
A request containing a textual query from the user or an event which should
be processed by the dialogue manager.
The last state to continue from is provided in the `tracker` field.

**Note:** Only one of the fields `text` or `event` may be set at a time.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  | A key for selecting the desired dialogue manager |
| tracker | [bytes](#bytes) |  | The last dialog state from the previous call. If this is the first call, this field must be left empty. |
| sender_id | [string](#string) |  | UUID for identifying the user |
| text | [string](#string) |  | Textual query from the user |
| debug | [bool](#bool) |  | True, if debug information for this request should also be returned |






<a name="speaker.beta2.DialogueResponse"></a>

### DialogueResponse
The response to the DialogueRequest which in any case contains the current
dialogue state (`tracker`), possibly a reply (`text`) and/or a list of events and
a follow up action.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| tracker | [bytes](#bytes) |  | dialogue state after processing the current request |
| text | [string](#string) |  | textual reply to the request |
| events | [google.protobuf.Struct](#google.protobuf.Struct) | repeated | A list of client-specific events triggered by the request |
| follow_up | [bool](#bool) |  | true, if the service expects further input from the user |
| debug_info | [google.protobuf.Struct](#google.protobuf.Struct) |  | Debug information needed to reconstruct the request in case of an error. |






<a name="speaker.beta2.SpeechRecognitionRequest"></a>

### SpeechRecognitionRequest
Request to transcribe an audio recording of the user.

**Note:** Only one of the fields `config` or `audio` may be set at a time.
The first message has to contain the `config` field and all subsequent
messages have to contain the `audio` field.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| config | [SpeechRecognitionRequest.Config](#speaker.beta2.SpeechRecognitionRequest.Config) |  | Speech recognizer configuration |
| audio | [bytes](#bytes) |  | Audio data |






<a name="speaker.beta2.SpeechRecognitionRequest.Config"></a>

### SpeechRecognitionRequest.Config



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| language | [string](#string) |  | The language with which the recognition should be performed |
| flavor | [string](#string) |  | (Optional) This field is intended for selecting a specialized language model, e.g. to better recognize technical terms |
| audio_format | [AudioFormat](#speaker.beta2.AudioFormat) |  | Format in which the audio data will be encoded |
| intermediate_results | [bool](#bool) |  | True, if intermediate transcription results should be returned |
| multiple_utterances | [bool](#bool) |  | True, if more than one user utterance should be transcribed; on False the recognizer will not transcribe anything after the first utterance is finished |
| debug | [bool](#bool) |  | True, if debug information for this request should also be returned |






<a name="speaker.beta2.SynthesizedSpeech"></a>

### SynthesizedSpeech
The synthesized speech; may be a stream of these messages.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| audio | [bytes](#bytes) |  | synthesized speech |
| debug_info | [google.protobuf.Struct](#google.protobuf.Struct) |  | Debug information needed to reconstruct the request in case of an error. |






<a name="speaker.beta2.Transcript"></a>

### Transcript
Transcribed text from the user's utterance


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text | [string](#string) |  | Transcription of the recording |
| utterance_finished | [bool](#bool) |  | Flag indicating whether this is the final recognition result |
| word_alignment | [Transcript.WordAlignment](#speaker.beta2.Transcript.WordAlignment) | repeated | A list of word WordAlignment messages for each word transcribed |
| debug_info | [google.protobuf.Struct](#google.protobuf.Struct) |  | Debug information needed to reconstruct the request in case of an error. |






<a name="speaker.beta2.Transcript.WordAlignment"></a>

### Transcript.WordAlignment
The word alignment describes the confidence, position and length of a recognized word


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| word | [string](#string) |  | A single word from the transcript (in order of appearance) |
| confidence | [float](#float) |  | The confidence score for the recognition of this word (between 0 and 1) |
| start | [float](#float) |  | Start offset of word within the audio recording (in seconds) |
| length | [float](#float) |  | Length of the word within the audio recording (in seconds) |
| original_transcript | [string](#string) |  | The transcript hypothesis this word originated from |






<a name="speaker.beta2.TtsRequest"></a>

### TtsRequest
A request to synthesize a given text as spoken language.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| text | [string](#string) |  | The utterance to be synthesized. |
| language | [string](#string) |  | The desired language in which the utterance is to be synthesized. |
| voice | [string](#string) |  | (Optional) The name of the voice; if not given the service will choose the language default. |
| audio_format | [AudioFormat](#speaker.beta2.AudioFormat) |  | The desired audio data format in which the synthesized speech is to be returned. |
| speech_rate | [float](#float) |  | Speed rate of the synthesized speech; if unset (0.0) it will default to 1.0 which is the regular speed. Values above 1.0 will result in faster pace, vice vera for values below. |
| debug | [bool](#bool) |  | True, if debug information for this request should also be returned |





 <!-- end messages -->

## Enums

<a name="speaker.beta2.AssistantResponse.FollowUp"></a>

### AssistantResponse.FollowUp
This enum describes the possible continuation of the dialogue.

| Name | Number | Description |
| ---- | ------ | ----------- |
| FOLLOW_UP_UNSPECIFIED | 0 | Field not set |
| EXPECT_SPEECH | 1 | The system expects a subsequent response from the user, i.e. the client should continue to record the user's utterances. |
| DIALOGUE_FINISHED | 2 | From the point of view of the assistant, the conversation is over, i.e. the client can stop recording and wait for the next keyword, for example. |



<a name="speaker.beta2.AudioFormat.Encoding"></a>

### AudioFormat.Encoding
This field describes the encoding of the incoming or outgoing audio data for the respective request.

| Name | Number | Description |
| ---- | ------ | ----------- |
| AUDIO_FORMAT_UNSPECIFIED | 0 | Field not set |
| WAV | 1 | RIFF WAVE |
| FLAC | 2 | Free Lossless Audio Codec (https://xiph.org/flac/) |


 <!-- end enums -->

 <!-- end HasExtensions -->



## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a name="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a name="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |

