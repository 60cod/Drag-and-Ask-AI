import openai
import logging

class AIService:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.logger = logging.getLogger('AIService')

    async def get_response(self, text):
        """
        OpenAI API를 호출하여 응답을 받아옵니다.
        """
        try:
            self.logger.info("API 호출 시작")
            
            # API 호출 전에 키 확인
            if not openai.api_key:
                raise ValueError("OpenAI API 키가 설정되지 않았습니다.")
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",  # 더 저렴한 모델 사용
                messages=[
                    {"role": "system", "content": "주어진 텍스트에 대해 매우 간결하게 핵심 정보만 설명해주세요. 서론과 결론은 생략하고 본론만 진중하게 답변하세요."},
                    {"role": "user", "content": f"다음 텍스트를 분석해주세요:\n{text}"}
                ],
                max_tokens=100,  # 토큰 수 제한
                temperature=0.5   # 더 일관된 응답을 위해 temperature 낮춤
            )
            
            if not response or not response.choices:
                raise ValueError("API 응답이 비어있습니다.")
                
            answer = response.choices[0].message.content
            self.logger.info("API 응답 받음")
            return answer
            
        except openai.error.AuthenticationError:
            self.logger.error("API 인증 오류: 잘못된 API 키")
            raise ValueError("OpenAI API 키가 유효하지 않습니다.")
            
        except openai.error.RateLimitError:
            self.logger.error("API 할당량 초과")
            raise ValueError("API 호출 한도를 초과했습니다. 잠시 후 다시 시도해주세요.")
            
        except Exception as e:
            self.logger.error(f"API 호출 오류: {str(e)}")
            raise 