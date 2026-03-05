import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'constants.dart';

class ApiClient {
  late Dio _dio;
  final _storage = const FlutterSecureStorage();

  ApiClient() {
    _dio = Dio(
      BaseOptions(
        baseUrl: ApiConstants.baseUrl,
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 10),
        contentType: 'application/json',
      ),
    );

    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          String? token = await _storage.read(key: 'token');
          if (token != null) {
            options.headers["Authorization"] = "Bearer $token";
          }
          return handler.next(options);
        },
        onError: (DioException e, handler) {
          return handler.next(_handleError(e));
        },
      ),
    );
  }

  // دالة POST (لإضافة بيانات أو تسجيل دخول)
  Future<Response> post(String path, dynamic data) async => await _dio.post(path, data: data);

  // دالة GET (لجلب البيانات)
  Future<Response> get(String path) async => await _dio.get(path);

  // دالة PUT (لتعديل بيانات موجودة) - ضرورية لإصلاح واجهة التعديل
  Future<Response> put(String path, dynamic data) async => await _dio.put(path, data: data);

  // دالة DELETE (لحذف بيانات) - ضرورية لواجهة الحذف
  Future<Response> delete(String path) async => await _dio.delete(path);

  DioException _handleError(DioException e) {
    String errorMessage = "Something went wrong";
    if (e.type == DioExceptionType.connectionTimeout) {
      errorMessage = "Connection timeout";
    } else if (e.response != null) {
      errorMessage = e.response?.data['detail'] ?? "Server error";
    }
    return DioException(
      requestOptions: e.requestOptions,
      error: errorMessage,
      response: e.response,
    );
  }
}