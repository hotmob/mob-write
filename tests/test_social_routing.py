"""Structural checks for social scene routing.

These tests read the public instructions. They do not score a draft and do not
claim that a model followed the guidance.
"""

import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_chatgpt as builder  # noqa: E402


SOCIAL_GUIDES = (
    "SKILL.md",
    "references/social.md",
    "references/social-posts.md",
    "references/social-commentary.md",
    "references/sources.md",
)

# Positive claims from the separate local note. Negations that reject them are allowed.
UNSUPPORTED_CLAIMS = (
    "收藏不参与",
    "分享链接权重",
    "80–180",
    "80-180",
    "用网页或 App",
    "seeded_replies",
    "exposure_research",
    "原创每天最多",
    "用“大多数人 vs 高手”",
)


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


class SocialRoutingTests(unittest.TestCase):
    def test_entry_selects_social_without_replacing_other_routes(self):
        skill = read("SKILL.md")
        self.assertEqual(skill.count("name: mob-write"), 1)
        self.assertNotIn("x-viral-writing", skill)
        self.assertIn("references/social.md", skill)
        self.assertIn("choose the deliverable first", skill)
        self.assertIn("Ordinary factual questions alone in any language", skill)
        self.assertIn("every social subguide", skill)
        self.assertIn("Apply only to the Chinese portion", skill)
        self.assertIn("references/work.md", skill)
        self.assertIn("references/technical-document.md", skill)
        self.assertIn("Do not invent", skill)
        self.assertIn("Preserve explicitly supplied uncertainty", skill)

    def test_social_index_has_one_owner_for_reference_selection(self):
        social = read("references/social.md")
        rows = [line for line in social.splitlines() if line.startswith("| ")]
        def route(label):
            return next(row for row in rows if label in row).split("|")[2]
        self.assertNotIn("social-", route("普通回复"))
        self.assertIn("social-commentary.md", route("给原作者的直接回复"))
        self.assertIn("不读帖子成稿", route("给原作者的直接回复"))
        self.assertIn("social-posts.md", route("原创短帖"))
        self.assertIn("才先读评论", route("原创短帖"))
        self.assertIn("不读帖子成稿", route("不交付帖子"))
        self.assertIn("不读社交参考", route("工作邮件"))
        self.assertIn("先读评论，再读帖子成稿，每份只读一次", social)
        self.assertNotIn("(social-commentary.md)", read("references/social-posts.md"))
        self.assertNotIn("(social-posts.md)", read("references/social-commentary.md"))

    def test_short_posts_are_not_forced_into_headlines_or_nicknames(self):
        posts = read("references/social-posts.md")
        self.assertIn("普通短帖默认不另加标题", posts)
        self.assertIn("Article、长文，或用户明确要求标题时，另拟标题", posts)
        self.assertIn("不复制成短帖标题", posts)
        self.assertIn("前两行", posts)
        self.assertIn("钩子必须真实，正文要兑现", posts)
        self.assertIn("Google Gemini4Neon", posts)
        self.assertIn("单独的 Neon", posts)
        self.assertIn("不表示该名称下有任何已核实的产品事实", posts)
        self.assertIn("不要求每条都有数字", posts)
        self.assertIn("不要求每条配图", posts)
        self.assertIn("不用“大多数人”对“高手”", posts)
        self.assertIn("我更在意", posts)
        self.assertIn("未经验证的推荐权重", posts)

    def test_commentary_uses_three_dimensions_without_a_three_part_draft(self):
        commentary = read("references/social-commentary.md")
        for dimension in ("开发者", "AI 行业", "社会"):
            self.assertIn(dimension, commentary)
        self.assertIn("不要求写成三段", commentary)
        self.assertIn("不成为短帖标题", commentary)
        self.assertIn("已观察的事实、厂商或客户的声称、作者自己的推断要分开写", commentary)
        self.assertIn("单个案例不能推广成普遍收益", commentary)
        self.assertIn("演示耗时不是生产部署成本", commentary)
        self.assertIn("不能把差异全部归因于环境", commentary)
        self.assertIn("会改变读者理解或判断的条件", commentary)
        self.assertIn("不为每句推断附上重复的免责声明", commentary)
        self.assertIn("我更在意", commentary)
        self.assertIn("因果", commentary)
        self.assertIn("不必把整条因果链铺成一长串", commentary)

    def test_commentary_states_supported_judgment_without_filler(self):
        commentary = read("references/social-commentary.md")
        self.assertIn("这是 Google 公布的结果", commentary)
        self.assertIn("不表示任何一次发布的出处", commentary)
        self.assertIn("把模型、工具和工作台一起测", commentary)
        self.assertIn("不能把它补在新闻后面", commentary)
        self.assertIn("真正争夺的是……", commentary)
        self.assertIn("X 要争的，还有……", commentary)
        self.assertIn("不固定每条都用“我看”", commentary)
        self.assertIn("我看甲公司是想靠模型，把开发者留在自己的生态体系里。", commentary)
        self.assertIn("不提供产品事实", commentary)
        self.assertIn("不许把原句或“生态体系”套到别的新闻上", commentary)
        examples = read("examples/social.md")
        self.assertIn("这是灯塔实验室公布的结果", examples)
        self.assertIn("还不能当成其他店已经省下的时间", examples)

    def test_other_scenes_remain_addressed(self):
        self.assertIn("不把评论改写成工作邮件", read("references/work.md"))
        technical = read("references/technical-document.md")
        self.assertIn("社交平台上的新闻或技术短评走 [社交接话](social.md)", technical)
        self.assertIn("不因出现产品名就改用本文件", technical)

    def test_unsupported_algorithm_claims_are_not_written_as_rules(self):
        combined = "\n".join(read(path) for path in SOCIAL_GUIDES)
        for claim in UNSUPPORTED_CLAIMS:
            self.assertNotIn(claim, combined)
        sources = read("references/sources.md")
        self.assertIn("x-viral-writing", sources)
        self.assertIn("not a second entry", sources)
        self.assertIn("recommender weights", sources)
        self.assertIn("are not writing rules", sources)

    def test_public_guides_do_not_carry_private_account_material(self):
        private = re.compile(
            r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|/Users/|/home/|exposure_research|seeded_replies"
        )
        for relative in (
            *SOCIAL_GUIDES,
            "examples/social.md",
            "references/work.md",
            "references/technical-document.md",
        ):
            self.assertIsNone(private.search(read(relative)), relative)

    def test_synthetic_examples_show_the_new_boundaries(self):
        examples = read("examples/social.md")
        self.assertTrue(examples.startswith("# Social examples"))
        self.assertIn("All cases below are synthetic.", examples)
        self.assertIn("## S3 —", examples)
        self.assertIn("## S4 —", examples)
        self.assertIn("北风软件", examples)
        self.assertIn("灯塔实验室", examples)
        self.assertIn("短帖不另加标题", examples)
        self.assertIn("不写成三段", examples)

    def test_subguides_are_part_of_the_public_package(self):
        self.assertIn("references/social-posts.md", builder.SKILL_FILES)
        self.assertIn("references/social-commentary.md", builder.SKILL_FILES)


if __name__ == "__main__":
    unittest.main()
