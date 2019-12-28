auto()

/*
flag = click("手机淘宝") // 打开淘宝
sleep(15000)
click(803,1309) // 进入双11盖楼
sleep(15000)
*/

/*
    从双11盖楼页面开始
    注意：清理后台
*/

click(545,1381) // 领喵币(中心)
sleep(500)
click(911,1723) // 领喵币(右下角)
sleep(2000)
click("签到")
sleep(2000)

/*
    微信分享
*/
click("去分享")
sleep(5000)
click("微信")
sleep(5000)
click(548,1146) // 粘贴给好友
sleep(5000)
click("魏一鸣、李俊晖")
sleep(2000)
text(getClip())
sleep(2000)
click("发送")
sleep(2000)
back()
sleep(500)
back()
sleep(2000)
recents()
sleep(2000)
click("手机淘宝")
sleep(2000)
back()
sleep(2000)

for (var i = 0; i < 50; i++){
    sleep(1000);

    flag = click("去浏览")
    if (flag){
        sleep(24000);
        back();
    }

    flag2 = click("去进店")
    if (flag2){
        sleep(26000);
        back();
    }

    flag3 = click("去签到")
    if (flag3){
        sleep(15000)
        click(916,1146) // 领取奖励
        back()
    }

    if (flag == false && flag2 == false && flag3 == false){
        break;
    }
}

toast("完成")







