from PIL import Image


class PolicyHandImage:
    def __init__(self, policy1: str, policy2: str, policy3: str):
        self._policies_ = [policy1, policy2, policy3]
        self._generated_image_ = None

    def compose(self):
        img1 = Image.open('secret_hitler/img/policy_liberal.png')
        img1 = img1.resize((292, 450))
        img2 = Image.open('secret_hitler/img/policy_fascist.png')
        img2 = img2.resize((292, 450))

        new_size = 3 * 292 + 20

        img_new = Image.new('RGBA', (new_size, 470), (255, 0, 0, 0))
        if self._policies_[0] == 'L':
            img_new.paste(img1, (10, 10))
        else:
            img_new.paste(img2, (10, 10))

        if self._policies_[1] == 'L':
            img_new.paste(img1, (292 + 10, 10))
        else:
            img_new.paste(img2, (292 + 10, 10))

        if self._policies_[2] == 'L':
            img_new.paste(img1, (2 * 292 + 10, 10))
        else:
            img_new.paste(img2, (2 * 292 + 10, 10))
        self._generated_image_ = img_new

    def write(self, fp: str):
        if self._generated_image_ is not None:
            self._generated_image_.save(fp)
