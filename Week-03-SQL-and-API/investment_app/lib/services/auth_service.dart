import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../core/api_client.dart';
import '../core/constants.dart';

class AuthService {
  final ApiClient _apiClient = ApiClient();
  final _storage = const FlutterSecureStorage();

  // --- تسجيل الدخول ---
  Future<bool> login(String email, String password) async {
    try {
      final formData = FormData.fromMap({
        "username": email,
        "password": password,
      });

      final response = await _apiClient.post(
        ApiConstants.loginEndpoint,
        formData,
      );

      if (response.statusCode == 200) {
        String token = response.data['access_token'];
        await _storage.write(key: 'token', value: token);
        return true;
      }
      return false;
    } on DioException catch (e) {
      _handleDioError(e); // دالة معالجة الأخطاء الموحدة
      rethrow;
    }
  }

  // --- إنشاء حساب جديد (الإصلاح هنا) ---
  Future<bool> register(String username, String email, String password) async {
    try {
      // السيرفر عادة يتوقع JSON في الـ Register وليس FormData
      final response = await _apiClient.post(
        ApiConstants.registerEndpoint, // تأكد من تعريف هذا في constants.dart
        {
          "username": username,
          "email": email,
          "password": password,
        },
      );

      return response.statusCode == 200 || response.statusCode == 201;
    } on DioException catch (e) {
      _handleDioError(e);
      rethrow;
    }
  }

  // --- دالة سحرية لمعالجة أخطاء FastAPI وتجنب خطأ الـ List/String ---
  void _handleDioError(DioException e) {
    if (e.response != null && e.response?.data != null) {
      final data = e.response?.data;

      // FastAPI يرسل الأخطاء غالباً في حقل 'detail'
      var detail = data['detail'];

      if (detail is List) {
        // إذا كان الخطأ قائمة (Validation Error)، نأخذ أول رسالة خطأ
        // هذا هو السطر الذي سيحل مشكلة 'List is not a subtype of String'
        String message = detail.map((error) => error['msg']).join(", ");
        print("Backend Validation Error: $message");
        throw message;
      } else if (detail is String) {
        throw detail;
      }
    }
    throw "An unexpected error occurred";
  }

  Future<void> logout() async {
    await _storage.delete(key: 'token');
  }

  Future<bool> isLoggedIn() async {
    String? token = await _storage.read(key: 'token');
    return token != null;
  }
}