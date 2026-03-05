import 'package:flutter/material.dart';
import '../../core/api_client.dart';
import '../../core/constants.dart';

class AddAssetScreen extends StatefulWidget {
  const AddAssetScreen({super.key});

  @override
  _AddAssetScreenState createState() => _AddAssetScreenState();
}

class _AddAssetScreenState extends State<AddAssetScreen> {
  final _symbolController = TextEditingController();
  final _nameController = TextEditingController();
  final _quantityController = TextEditingController();
  final _priceController = TextEditingController();
  final _apiClient = ApiClient();
  bool _isLoading = false;

  void _saveAsset() async {
    // التحقق من إدخال البيانات
    if (_symbolController.text.isEmpty || _quantityController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please fill in the required fields")),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      // لاحظ استخدام ApiConstants.assetsList (أو المسمى الذي وضعته في ملف الـ Constants)
      await _apiClient.post(ApiConstants.assetsList, {
        "symbol": _symbolController.text.toUpperCase(),
        "asset_name": _nameController.text,
        "quantity": double.parse(_quantityController.text),
        "purchase_price": double.parse(_priceController.text),
      });

      if (mounted) {
        Navigator.pop(context, true); // إرجاع قيمة true لتحديث القائمة في الشاشة السابقة
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error: $e"), backgroundColor: Colors.redAccent),
      );
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text("Add New Asset", style: TextStyle(fontWeight: FontWeight.bold)),
        elevation: 0,
        backgroundColor: Colors.transparent,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          children: [
            _buildCustomField("Symbol (e.g., BTC)", Icons.token, _symbolController),
            const SizedBox(height: 15),
            _buildCustomField("Asset Name", Icons.label_outline, _nameController),
            const SizedBox(height: 15),
            _buildCustomField("Quantity", Icons.pie_chart_outline, _quantityController, isNumber: true),
            const SizedBox(height: 15),
            _buildCustomField("Purchase Price", Icons.attach_money, _priceController, isNumber: true),
            const SizedBox(height: 40),
            _isLoading
                ? const CircularProgressIndicator()
                : SizedBox(
              width: double.infinity,
              height: 55,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF0D47A1),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                ),
                onPressed: _saveAsset,
                child: const Text("Save to Portfolio",
                    style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCustomField(String label, IconData icon, TextEditingController controller, {bool isNumber = false}) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(15),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, 5))],
      ),
      child: TextField(
        controller: controller,
        keyboardType: isNumber ? const TextInputType.numberWithOptions(decimal: true) : TextInputType.text,
        decoration: InputDecoration(
          prefixIcon: Icon(icon, color: const Color(0xFF1E88E5)),
          labelText: label,
          border: InputBorder.none,
          contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
        ),
      ),
    );
  }
}