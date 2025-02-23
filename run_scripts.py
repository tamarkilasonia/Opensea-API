from database_app.models import Collection, Cars

# i created a table collection
#Collection.create_table()

# Collection.remove_columns("new_column")

# records = Collection.filter(name__icontains="Modern Art Collection")

# for i in records:
#     print(i.name)
#     print(i.contracts)

#     print("\n")
#     print("---- next ----")

# for i in collections_instance:
#     print(i.name)


# new_collection = Collection(
#     collection="Art NFTs1",
#     name="Modern Art Collection",
#     description="A collection of modern NFT artworks.",
#     image_url="https://example.com/image.jpg",
#     owner="0x123456...",
#     twitter_username="nft_artist",
#     contracts="[{\"address\": \"0x123456...\", \"chain\": \"ethereum\"}]"
# )

# new_collection2 = Collection(
#     collection="Art NFTs2",
#     name="Modern Art Collection",
#     description="A collection of modern NFT artworks.",
#     image_url="https://example.com/image.jpg",
#     owner="0x123456...",
#     twitter_username="nft_artist",
#     contracts="[{\"address\": \"0x123456...\", \"chain\": \"ethereum\"}]"
# )

# new_collection3 = Collection(
#     collection="Art NFTs3",
#     name="Modern Art Collection",
#     description="A collection of modern NFT artworks.",
#     image_url="https://example.com/image.jpg",
#     owner="0x123456...",
#     twitter_username="nft_artist",
#     contracts="[{\"address\": \"0x123456...\", \"chain\": \"ethereum\"}]"
# )

# Collection.bulk_insert([new_collection, new_collection2, new_collection3])

# collections = Collection.all()

# for i in collections:
#     print(f"name: {i.name}")



# populate json files
# load database

# from handle_etl.etl_pipeline import run_etl

# if __name__ == "__main__":
#     run_etl()



#################### testing delete method ########################

#print(Cars.all())
