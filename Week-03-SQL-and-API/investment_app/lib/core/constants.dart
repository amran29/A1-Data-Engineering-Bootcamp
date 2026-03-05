
class ApiConstants {
  // إذا كنت تستخدم محاكي الأندرويد، استخدم 10.0.2.2
  // إذا كنت تستخدم محاكي iOS أو متصفح الكروم، استخدم 127.0.0.1
  static const String baseUrl = "http://10.0.2.2:8000";

  // Auth Endpoints
  static const String loginEndpoint = "/auth/login";
  static const String signupEndpoint = "/auth/signup";

  // Portfolio Endpoints
  static const String portfolioSummary = "/portfolio/summary";
  static const String assetsEndpoint = "/assets/";
  static const String registerEndpoint = "/auth/signup";
  static const String assetsList = "/assets/";
}

class AppDesign {
  // إعدادات الألوان المركزية لتسهيل تغيير "ثيم" التطبيق مستقبلاً
  static const int primaryBlue = 0xFF1E88E5;
  static const int darkBlue = 0xFF0D47A1;
  static const int backgroundColor = 0xFFF5F7FA;
}