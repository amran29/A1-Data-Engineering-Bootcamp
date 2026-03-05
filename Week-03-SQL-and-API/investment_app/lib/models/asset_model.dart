class AssetModel {
  final int? id;
  final String symbol;
  final String assetName;
  final double quantity;
  final double purchasePrice;

  AssetModel({
    this.id,
    required this.symbol,
    required this.assetName,
    required this.quantity,
    required this.purchasePrice,
  });

  // تحويل البيانات القادمة من الباك اند (Map) إلى كائن AssetModel
  factory AssetModel.fromJson(Map<String, dynamic> json) {
    return AssetModel(
      id: json['id'],
      symbol: json['symbol'],
      assetName: json['asset_name'],
      // نستخدم .toDouble() لضمان عدم حدوث خطأ إذا أرسل السيرفر رقماً صحيحاً
      quantity: (json['quantity'] as num).toDouble(),
      purchasePrice: (json['purchase_price'] as num).toDouble(),
    );
  }
}