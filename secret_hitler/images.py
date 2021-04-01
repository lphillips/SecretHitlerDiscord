from PIL import Image


class PolicyHandImage:

    def __init__(self, policies: [str]):
        self._policies_ = policies
        self._generated_image_ = None

    def compose(self):
        img1 = Image.open('secret_hitler/img/policy_liberal.png')
        img1 = img1.resize((292, 450))
        img2 = Image.open('secret_hitler/img/policy_fascist.png')
        img2 = img2.resize((292, 450))

        img = {"L": img1, "F": img2}
        new_size = len(self._policies_) * 292 + 20

        img_new = Image.new('RGBA', (new_size, 470), (255, 0, 0, 0))

        for count, policy in enumerate(self._policies_):
            policy_img = img[policy]
            img_new.paste(policy_img, ((count * 292) + 10, 10))
        self._generated_image_ = img_new

    def write(self, fp: str):
        if self._generated_image_ is not None:
            self._generated_image_.save(fp)
