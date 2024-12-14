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
            "https://images.avto.net/photo/20178302/1044371.jpg",
            "https://images.avto.net/photo/20178302/2044394.jpg",
            "https://images.avto.net/photo/20178302/3044426.jpg",
            "https://images.avto.net/photo/20178302/4044448.jpg",
            # "https://images.avto.net/photo/20178302/5044490.jpg",
            "https://images.avto.net/photo/20178302/6044473.jpg",
            "https://images.avto.net/photo/20178302/7044513.jpg",
            "https://images.avto.net/photo/20178302/8044530.jpg",
            "https://images.avto.net/photo/20178302/8044531.jpg",
        ]

        vehicle = session.get(VehicleDB, vehicle_id)

        if vehicle.images:
            old_images_urls = [(image.index, image.avtonet_url) for image in vehicle.images]

            # Check if any changes were made to images
            if old_images_urls == images:
                print("true")
            else:
                # Check if any image were removed
                already_removed_images = [image for image in vehicle.images if image.removed]
                newly_removed_images = [
                    img
                    for img in vehicle.images
                    if (img.avtonet_url not in images)
                    and (img not in already_removed_images)
                ]
                for img in newly_removed_images:
                    # Mark that image as removed
                    img.removed = True

                # Check if any image was added
                if len(images) > len(old_images_urls):
                    for index, url in enumerate(images):
                        # Create new images if needed
                        if url not in old_images_urls:
                            img = ImageDB(avtonet_url=url, index=index)
                            vehicle.images.insert(index, img)
                        # Apply new image order
                        vehicle.images[index].index = index



                # for index, url in enumerate(images):
                #     try:
                #         old_img = old_images_urls[index]
                #     except IndexError:
                #         pass

                #     if (index, url) != old_img:

                # Go through new images
                # for index, url in enumerate(images):
                #     try:
                #         old_img = old_images[index]
                #     except IndexError:
                #         break

                #     print((index, url), old_img)
                #     # If there was new image uploaded
                #     if (index, url) != old_img:
                #         new_images.append((index, url))
                #     # # Else remove that image
                #     # elif url not in hidden_images:
                #     #     old_images.remove((index, url))

                # # If old_images_urls is not empty, it means that some image was removed, but it is still in db. Keep those images, but marked them as hidden
                # if old_images:
                #     pass
                # print([obj.__str__() for obj in new_image_objects])

                # session.add_all(new_image_objects)
                session.commit()

        else:
            for index, url in enumerate(images):
                image = ImageDB(avtonet_url=url, vehicle=vehicle, index=index)
                session.add(image)

            session.commit()
