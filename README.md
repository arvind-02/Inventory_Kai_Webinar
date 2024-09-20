## Setting Up SingleStore Kai
To set up SingleStore Kai:

1. Sign up for a SingleStore account at https://www.singlestore.com/
2. Create a new workspace only if you are using a credit based trial. If you signed up for a free tier the workspace and database will be created for you by default.
3. Within the workspace create a database called "Inventory"
4. Take note of the connection URL and the name of your database

## Set up Mongo
1. Navigate to your MongoDB Atlas portal and initiate a cluster. Within the cluster, create a database called "Inventory"
2. Take note of the connection URL and the name of your database

## Set up App
1. Clone the repository: git clone https://github.com/arvind-02/Inventory_Kai_Webinar.git
   
2. Navigate to the backend directory. Set up a .env file with the following environment variables:
   a. MONGO_LINK: the connection string for your mongo cluster
   b. OPENAI_API_KEY: your openAI api key
   c. MONGO_DATABASE: Whatever you decided to name your Mongo database, we suggested "Inventory"
   d. KAI_LINK: the connection string for your kai cluster
   e. KAI_DATABASE: Whatever you decided to name your Kai database, we suggested "Inventory"

3. Set up a virtual environment: `python -m venv venv`. Activate it by running `source venv/bin/activate`.
   
4. Navigate to the backend directory. Run `pip install -r requirements.txt`

5. Navigate to the frontend directory. Run `npm install`


## Generate Synthetic Data
1. Navigate to the data_creation directory within the backend directory
   
2. Run faker_user_data.py to create a users collection within your kai database and populate it with users. Adjust the num_users variable on line 30 to reflect how many users you want to generate. In our demo, we generate 3,000,000 users.
   
3. Run create_kai_products_collection.py to create a products collection within your kai database and place a vector index on the description_embedding field.

4. We have provided the products data we synthetically created within the category_products folder. However, if you want to see how this works yourself, run openai_generate_product_data.py. This will add products to a folder called category_products_new.

5. Run product_large_population.py to populate the products collection in kai. We have in total 10,500 products that we add, but you can choose to stop the script earlier if you don't want to add that many.

6. Run order_script.py to create an orders collection in your kai database. The script also generates orders to populate the collection with. Adjust the num_orders variable on line 27 to reflect how many orders you want to generate. Take the number of orders you want, and divide it by 3. For example, we wanted at lest 3 million orders, so we set the num_orders variable equal to 1,000,100

7. Run python transfer_data.py to populate your mongo database with the exact same data that's in your kai database.

8. To add more product vectors to stress test kai and mongo's vector search capabilities, run add_random_vectors.py. Adjust the num_embs value on line 25 based on how many vectors you want to add to your mongo and kai databases. In the webinar, we added around 300,000 extra products.

9. Run add_mongo_vector_index.py to add a vector index to the description_embedding field in your mongo products collection. In some Mongo cluster versions, you can't add an index through a python script. If this is the case for you, you can go the Mongo Atlas UI as well to add your index.

10. If at any point you want to drop some of your collections, run delete_collections.py. Set the kai_collections_drop variable on line 13 based on which kai collections you want to drop. Set the mongo_collections_drop variable on line 14 based on which mongo collections you want to drop. If you only want to drop some mongo collections but no kai collections, make sure the kai_collections_crop_variable is an empty list. This applies in reverse as well.

## Launch backend

Navigate to the backend directory and run: python main.py. You can view the backend at localhost:8000

## Launch frontend

Navigate to the frontend directory. Run: `npm run build` and then: `npm start` to launch the app. If you want to run the app in development mode, run: `npm run dev`. You can view your app at localhost:3000 !
