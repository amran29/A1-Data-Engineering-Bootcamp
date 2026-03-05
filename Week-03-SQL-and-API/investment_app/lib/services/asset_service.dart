import '../core/api_client.dart';
import '../models/asset_model.dart';
import '../core/constants.dart'; // تأكد من وجود هذا السطر لاستيراد الثوابت

class AssetService {
  final ApiClient _apiClient = ApiClient();

  // جلب البيانات
  Future<List<AssetModel>> fetchAssets() async {
    try {
      // نستخدم الثابت المعرف في ملف constants.dart
      final response = await _apiClient.get(ApiConstants.assetsEndpoint);

      List data = response.data;
      return data.map((json) => AssetModel.fromJson(json)).toList();
    } catch (e) {
      rethrow;
    }
  }

  // حذف أصل - نستخدم المسار الصحيح مع الـ ID
  Future<void> deleteAsset(int id) async {
    try {
      // تأكد أن المسار ينتهي بـ / ليكون الشكل /assets/5
      await _apiClient.delete("${ApiConstants.assetsEndpoint}$id");
    } catch (e) {
      rethrow;
    }
  }

  // تعديل أصل
  Future<void> updateAsset(int id, Map<String, dynamic> data) async {
    try {
      await _apiClient.put("${ApiConstants.assetsEndpoint}$id", data);
    } catch (e) {
      rethrow;
    }
  }
}