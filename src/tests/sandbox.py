import sys
from pathlib import Path

sys.path.append(str(Path.cwd().parent.absolute() / "src"))


from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from shared.models import Vehicle as VehicleDB
from shared.models import Seller as SellerDB
from shared.models import VehicleImage as ImageDB
from shared.config import settings


if __name__ == "__main__":
    engine = create_engine(settings.create_engine_url(), echo=False)

    with Session(engine) as session:
        vehicle_id = 20178302
        images = [
            "URL 1",
            "URL 4",
            "URL 2",
            "URL 3",
            # "https://images.avto.net/photo/20178302/1044371.jpg",
            # "https://images.avto.net/photo/20178302/2044394.jpg",
            # "https://images.avto.net/photo/20178302/3044426.jpg",
            # "https://images.avto.net/photo/20178302/4044448.jpg",
            # "https://images.avto.net/photo/20178302/5044490.jpg",
            # "https://images.avto.net/photo/20178302/6044473.jpg",
            # "https://images.avto.net/photo/20178302/7044513.jpg",
            # "https://images.avto.net/photo/20178302/8044530.jpg",
            # "https://images.avto.net/photo/20178302/8044531.jpg",
        ]

        seller = {
            "name": "AvtoPlanet",
            "seller_type": "company",
            "email": "mail@someone.si",
            "phone_numbers": [],
            "link": "link-to-something.com",
            "address": "Celjanova ulica 15, Celje",
            "seller_description": "lorem ipsum,.....",
            "avtonet_broker_id": 100230,
        }

        vehicle = session.get(VehicleDB, vehicle_id)

        # Process images
        if vehicle.images:
            vehicle.images.sort(key=lambda x: x.index)
            old_images_urls = [image.avtonet_url for image in vehicle.images]

            # Check if any changes were made to images
            if old_images_urls != images:
                # Check if any image were removed
                already_removed_images = [
                    image for image in vehicle.images if image.removed
                ]
                newly_removed_images = [
                    img
                    for img in vehicle.images
                    if (img.avtonet_url not in images)
                    and (img not in already_removed_images)
                ]
                for img in newly_removed_images:
                    # Mark that image as removed
                    img.removed = True
                    img.index = -1

                # Check if any image was added
                for index, url in enumerate(images):
                    # Create new images if needed
                    if url not in old_images_urls:
                        img = ImageDB(avtonet_url=url, index=index)
                        print("added", img)
                        vehicle.images.append(img)
                    # Apply new image order
                    else:
                        image_index = old_images_urls.index(url)
                        image = vehicle.images[image_index]
                        image.index = index
                        image.removed = False

                session.commit()
        else:
            for index, url in enumerate(images):
                image = ImageDB(avtonet_url=url, vehicle=vehicle, index=index)
                session.add(image)

            session.commit()

        # Process seller
