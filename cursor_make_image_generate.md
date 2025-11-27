이미지 생성 MCP Tool 추가해
- 입력 Parameter (단일): prompt
- 도구 호출 결과: base64-encoded-data image 형식

### API Document
```ts
import { InferenceClient } from "@huggingface/inference";

const client = new InferenceClient(process.env.HF_TOKEN);

const image = await client.textToImage({
    provider: "fal-ai",
    model: "black-forest-labs/FLUX.1-schnell",
	inputs: "Astronaut riding a horse",
	parameters: { num_inference_steps: 5 },
});
/// Use the generated image (it's a Blob)
```
 
### Tool Result
```json
{
  "type": "image",
  "data": "base64-encoded-data",
  "mimeType": "image/png"
  "annotations": {
    "audience": ["user"],
    "priority": 0.9
  }
}
```
