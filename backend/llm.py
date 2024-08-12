from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential
import os

GPT4o_mini = 'gpt-4o-mini'

class GPTEmailGenerator():
    def __init__(self, model=GPT4o_mini):
        
        self.client = OpenAI(
            api_key = os.environ.get('OPENAI_API_KEY')
        )
        self.model = model

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def _attempt_get_email(self, product_one_name, product_two_name, product_one_description, product_two_description, user_name):
        response = self.client.chat.completions.create(
          model=self.model,
          messages=[
                {"role": "system", "content": "You are Question Answering Portal"},
                {"role": "user", "content": f'''You are an expert at writing emails.
                 Pretend that you are an online store owner reaching out to a customer about a product. 
                 You saw a recent product that they bought, and you want to recommend a similar product to them.
                 You have a recommendation algorithm that recommends new products.
                 The first product the customer recently bought is {product_one_name}.
                 It's description is {product_one_description}.
                 The new product you want to recommend is {product_two_name}.
                 The description of this product is {product_two_description}.
                 The name of the customer is {user_name}.
                 The name of the online store is Singlestore E-Commerce.
                 Please write a 4-5 sentence email where you reach out to this customer and recommend buying this new product.
                 End the email with Best regards, Singlestore Ecommerce.'''}
            ],
          temperature=0.5
        )


        return response.choices[0].message.content


    @retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(6))
    def get_email(self, product_one_name, product_two_name, product_one_description, product_two_description, user_name):

        try:
            return self._attempt_get_email(product_one_name, product_two_name, product_one_description, product_two_description, user_name)
        except Exception as e:
            print(e)

'''
model = GPTEmailGenerator()
print(model.get_email("Laptop", 
                      "Tablet", 
                      "A high-performance laptop suitable for all your computing needs. It features a sleek design and powerful hardware, making it perfect for both work and entertainment.", 
                      "A versatile tablet with a vibrant display and long battery life. Ideal for browsing, reading, and on-the-go productivity.",
                      "Alice Johnson"))
                      '''