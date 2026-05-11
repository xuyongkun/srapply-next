from fastapi import APIRouter

router = APIRouter()


@router.get("/site-info")
def site_info() -> dict:
    return {
        "brand": "申荣留学",
        "slogan": "让留学更简单 · To Be Easier And Better",
        "about": {
            "intro": "申荣留学是壹佰(香港)教育集团全资控股的高端留学咨询品牌，专注于为每一位学生提供个性化、透明化的留学规划服务。我们致力于打破传统留学中介的信息壁垒，让优质海外教育资源触手可及。",
            "mission": "我们的使命是让留学服务更简单、更透明。从选校定位、背景提升、文书定制到签证指导、行前准备，申荣团队提供全流程一站式服务，用专业与真诚陪伴每一位学子的留学之路。",
        },
        "highlights": [
            {
                "title": "定位准确",
                "icon": "target",
                "desc": "基于学生背景与职业规划，精准匹配最适合的院校与专业，拒绝模板化方案。",
            },
            {
                "title": "服务周到",
                "icon": "heart",
                "desc": "从选校到行前，全流程一对一顾问跟进，7×24小时在线答疑，让家长更放心。",
            },
            {
                "title": "经验丰富",
                "icon": "star",
                "desc": "核心顾问团队平均从业年限超过8年，累计服务学生2000+，名校录取率行业领先。",
            },
            {
                "title": "与时俱进",
                "icon": "trending",
                "desc": "持续跟踪各国签证政策与院校招生动态，确保申请策略始终走在最前沿。",
            },
        ],
        "stats": [
            {"value": "10+", "label": "年行业经验"},
            {"value": "2000+", "label": "服务学生"},
            {"value": "98%", "label": "签证通过率"},
            {"value": "100+", "label": "合作院校"},
        ],
        "contact": {
            "email": "srapply@163.com",
            "phone": "18516222635",
            "wechat_hint": "提交咨询后实时通知微信客服",
        },
        "locations": [
            {
                "city": "成都",
                "district": "高新区",
                "address": "环球中心E2-5楼喵谷",
                "metro": "地铁1号线锦城广场站A口",
            },
            {
                "city": "成都",
                "district": "天府新区",
                "address": "天府二街166号雄川金融中心1栋19楼",
                "metro": "",
            },
            {
                "city": "南昌",
                "district": "",
                "address": "恒茂梦时代广场7号楼603室",
                "metro": "",
            },
            {
                "city": "香港",
                "district": "九龙",
                "address": "旺角亚皆老街98号富都大厦0222室",
                "metro": "",
            },
        ],
    }
