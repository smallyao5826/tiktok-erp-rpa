import json
from datetime import datetime
from dao.auth_dao import AuthDao
from service.promotion_service.add_promotion_service import AddPromotionService
from utils.logger_util import get_logger

logger = get_logger("SimpleTest")

def run_simple_test():
    # --- 配置参数 ---
    SHOP_ID = "9648818"
    PRODUCT_ID = "1732253861680550744"
    
    # 实例化组件
    auth_dao = AuthDao()
    add_service = AddPromotionService()

    print("\n" + "="*30)
    print("🚀 极简促销测试启动 (指定时段版)")
    print("="*30 + "\n")

    # 1. 检查数据库中已有的 Cookie
    profile = auth_dao.get_profile()
    if not profile or not profile.get("cookie"):
        print("❌ 错误：数据库里没有发现 Cookie，请确认 auth_profile 表是否有数据。")
        return

    logger.info(f"使用现有账户: {profile['account']}")

    # 2. 准备指定的时间段 (PST 时间)
    # 🎯 修改点：手动指定 4月11日 00:00-00:59
    start_time = "2026-04-11 00:00:00"
    end_time = "2026-04-11 00:59:59"
    
    time_slots = [{"start": start_time, "end": end_time}]
    logger.info(f"设定测试时段: {start_time} 至 {end_time}")

    # 3. 执行创建
    logger.info(f"正在为店铺 {SHOP_ID} 创建单商品闪购...")
    
    res = add_service.create_batch_flash_sales(
        shop_id=SHOP_ID,
        time_slots=time_slots,
        platform_item_ids=[PRODUCT_ID],
        discount_rate=0.5
    )

    # 4. 打印结果
    if res.get("result") == "success":
        print("\n✅ 闪购创建成功！")
        # 此时标题应该类似：A3-2026.4.11-00:00-00:59-S1-XX
        print(f"活动 ID: {res['report']['success_slots'][0]['ids']}")
        if res['report'].get("fail_details"):
             print(f"⚠️ 注意：部分提交存在问题: {res['report']['fail_details']}")
    else:
        print(f"\n❌ 创建失败: {res.get('reason')}")
        if res.get("details"):
            print(f"📄 真实错误原因: {json.dumps(res['details'], ensure_ascii=False, indent=2)}")

if __name__ == "__main__":
    run_simple_test()