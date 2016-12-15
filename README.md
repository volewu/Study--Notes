# 学习--Notes
自已收集有关androd的知识点与开源项目
##Android APK 瘦身
1.[Android APK瘦身经验总结](http://www.jianshu.com/p/bfe44ef18aca)

2.[使用Android Studio的lint清除无用的资源文件](http://waychel.com/shi-yong-android-studiode-lintqing-chu-wu-yong-de-zi-yuan-wen-jian/)

##Android 官方 Lambda
1.方法 ： 
module下边的build.gradle配置 
android { 
　　compileSdkVersion 23 
　　buildToolsVersion “24.0.0”//24.0.0及以上 
　　defaultConfig { 
　　　　applicationId “bf.myapplication” 
　　　　minSdkVersion 23 
　　　　targetSdkVersion 23 
　　　　versionCode 1 
　　　　versionName “1.0” 
　　　　//jack必须 
　　　　jackOptions { 
　　　　　　enabled true　　 
　　　　} 
　　} 
　　buildTypes { 
　　　　release { 
　　　　　　minifyEnabled false 
　　　　　　proguardFiles getDefaultProguardFile(‘proguard-android.txt’), ‘proguard-rules.pro’ 
　　　　} 
　　} 
　　//使用java1.8 
　　compileOptions { 
　　　　sourceCompatibility JavaVersion.VERSION_1_8 
　　　　targetCompatibility JavaVersion.VERSION_1_8 
　　} 
}

##RecyclerVeiw 学习知识点。
1.[深入浅出 RecyclerView](http://kymjs.com/code/2016/07/10/01)
