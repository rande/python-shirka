from responders import Responder

import unittest

class RagefaceResponder(Responder):
    IMG = {
        "badumtss": "http://res.cloudinary.com/ragekino/image/upload/v1362760929/troll_ba_dum_tss_s_creewj.png",
        "cerealguy": "http://res.cloudinary.com/ragekino/image/upload/v1362760896/cereal_guy_cereal_guy_spitting_s_hhpkji.png",
        "cute": "http://res.cloudinary.com/ragekino/image/upload/v1362760895/cat_cat_overload_s_qmx7vg.png",
        "deskflip": "http://res.cloudinary.com/ragekino/image/upload/v1362760891/angry_desk_flip_s_esu2sj.png",
        "fuckyeah": "http://res.cloudinary.com/ragekino/image/upload/v1362760903/fuck_yeah_fuck_yeah_clean_s_q6zhjp.png",
        "genius": "http://res.cloudinary.com/ragekino/image/upload/v1362760911/misc_genius_s_smgot2.png",
        "itssomething": "http://res.cloudinary.com/ragekino/image/upload/v1362760917/neutral_its_something_s_ytrs7y.png",
        "lol": "http://res.cloudinary.com/ragekino/image/upload/v1362760908/laughing_lol_crazy_s_x6hjhg.png",
        "longneck": "http://res.cloudinary.com/ragekino/image/upload/v1362760926/surprised_long_neck_surprise_s_xcrggy.png",
        "megusta": "http://res.cloudinary.com/ragekino/image/upload/v1362760909/me_gusta_me_gusta_s_fuqfcn.png",
        "notbad": "http://res.cloudinary.com/ragekino/image/upload/v1362760920/obama_really_not_bad_s_nkkjic.png",
        "nothing": "http://res.cloudinary.com/ragekino/image/upload/v1362760913/misc_nothing_to_do_here_s_onqypc.png",
        "pokerface": "http://res.cloudinary.com/ragekino/image/upload/v1362760918/neutral_poker_face_no_text_s_shbpto.png",
        "rageguy": "http://res.cloudinary.com/ragekino/image/upload/v1362760923/rage_rage_s_gwrlyy.png",
        "sir": "http://res.cloudinary.com/ragekino/image/upload/v1362760916/neutral_feel_like_a_sir_clean_s_bgjky3.png",
        "troll": "http://res.cloudinary.com/ragekino/image/upload/v1362760933/troll_troll_face_s_kshfjf.png",
        "true": "http://res.cloudinary.com/ragekino/image/upload/v1362760915/misc_true_story_realistic_s_fq1lev.png",
        "win": "http://res.cloudinary.com/ragekino/image/upload/v1362760911/misc_freddie_mercury_s_ydyqcx.png",
        "bitch": "http://res.cloudinary.com/ragekino/image/upload/v1362760901/fuck_that_bitch_fuck_that_shit_female_s_ivczxv.png",
        "ragenuclear": "http://res.cloudinary.com/ragekino/image/upload/v1362760922/rage_nuclear_s_yjdskn.png",
    }

    def support(self, message):
        return message[0:4] == 'face'

    def generate(self, message):
        words = message.split(" ")

        if len(words) < 2:
            return False

        if words[1] == 'help':
            return "Face available: %s" % (", ".join(RagefaceResponder.IMG))

        if words[1] in RagefaceResponder.IMG:
            return RagefaceResponder.IMG[words[1]]

        return False


class TestRagefaceResponder(unittest.TestCase):
    def setUp(self):
        self.responder = RagefaceResponder()

    def test_support(self):
        self.assertTrue(self.responder.support("face"))
        self.assertFalse(self.responder.support("fuu"))

    def test_incomplete_command(self):
        self.assertFalse(self.responder.generate("face"))

    def test_help(self):
        self.assertIsNotNone(self.responder.generate("face help"))

    def test_valid(self):
        self.assertEquals(self.responder.generate("face win"), "http://fuuu.us/188.png")
