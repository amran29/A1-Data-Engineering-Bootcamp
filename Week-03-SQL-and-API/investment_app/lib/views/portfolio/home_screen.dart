import 'package:flutter/material.dart';
import 'package:shimmer/shimmer.dart';
import '../../services/auth_service.dart';
import '../../services/asset_service.dart';
import '../../models/asset_model.dart';
import '../auth/login_screen.dart';
import 'add_asset_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final AuthService _authService = AuthService();
  final AssetService _assetService = AssetService();

  List<AssetModel> _assets = [];
  double _totalBalance = 0.0;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  // حساب الرصيد الإجمالي بشكل منفصل
  void _calculateTotal(List<AssetModel> assets) {
    _totalBalance = assets.fold(0, (sum, item) => sum + (item.quantity * item.purchasePrice));
  }

  Future<void> _loadData() async {
    if (!mounted) return;
    setState(() => _isLoading = true);
    try {
      final fetchedAssets = await _assetService.fetchAssets();
      setState(() {
        _assets = fetchedAssets;
        _calculateTotal(_assets);
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      _showSnackBar("Connection Error: $e", Colors.redAccent);
    }
  }

  // حذف "متفائل" - يحذف من الواجهة أولاً لسرعة الاستجابة
  void _handleDelete(int id) async {
    final originalAssets = List<AssetModel>.from(_assets);

    setState(() {
      _assets.removeWhere((asset) => asset.id == id);
      _calculateTotal(_assets);
    });

    try {
      await _assetService.deleteAsset(id);
      _showSnackBar("Asset removed", Colors.blueGrey);
    } catch (e) {
      // إذا فشل الحذف في السيرفر، نعيد البيانات كما كانت
      setState(() {
        _assets = originalAssets;
        _calculateTotal(_assets);
      });
      _showSnackBar("Failed to delete. Try again.", Colors.red);
    }
  }

  void _showSnackBar(String message, Color color) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: color,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        margin: const EdgeInsets.all(15),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: _buildAppBar(),
      floatingActionButton: _buildFAB(),
      body: RefreshIndicator(
        onRefresh: _loadData,
        color: const Color(0xFF0D47A1),
        child: CustomScrollView(
          slivers: [
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: _BalanceCard(balance: _totalBalance),
              ),
            ),
            const SliverToBoxAdapter(
              child: Padding(
                padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                child: Text("My Portfolio", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Color(0xFF1E293B))),
              ),
            ),
            _isLoading ? _buildLoadingList() : _buildSliverList(),
          ],
        ),
      ),
    );
  }

  // قائمة الأصول باستخدام Sliver لمرونة التمرير
  Widget _buildSliverList() {
    if (_assets.isEmpty) {
      return SliverFillRemaining(child: _buildEmptyState());
    }
    return SliverPadding(
      padding: const EdgeInsets.symmetric(horizontal: 20),
      sliver: SliverList(
        delegate: SliverChildBuilderDelegate(
              (context, index) {
            final asset = _assets[index];
            return _AssetListItem(
              asset: asset,
              onDelete: () => _handleDelete(asset.id!),
              onTap: () => _showEditDialog(asset),
            );
          },
          childCount: _assets.length,
        ),
      ),
    );
  }

  // واجهة التحميل الوهمي (Shimmer)
  Widget _buildLoadingList() {
    return SliverPadding(
      padding: const EdgeInsets.symmetric(horizontal: 20),
      sliver: SliverList(
        delegate: SliverChildBuilderDelegate(
              (context, index) => Shimmer.fromColors(
            baseColor: Colors.grey[300]!,
            highlightColor: Colors.grey[100]!,
            child: Container(
              height: 80,
              margin: const EdgeInsets.only(bottom: 12),
              decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(15)),
            ),
          ),
          childCount: 5,
        ),
      ),
    );
  }

  // --- المكونات المستخرجة ---

  AppBar _buildAppBar() {
    return AppBar(
      title: const Text("Investo", style: TextStyle(color: Color(0xFF0D47A1), fontWeight: FontWeight.w900, letterSpacing: 1)),
      centerTitle: false,
      backgroundColor: Colors.transparent,
      elevation: 0,
      actions: [
        Container(
          margin: const EdgeInsets.only(right: 15),
          decoration: BoxDecoration(color: Colors.red[50], shape: BoxShape.circle),
          child: IconButton(
            icon: const Icon(Icons.logout_rounded, color: Colors.redAccent, size: 20),
            onPressed: () async {
              await _authService.logout();
              if (mounted) Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => LoginScreen()));
            },
          ),
        )
      ],
    );
  }

  Widget _buildEmptyState() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Opacity(opacity: 0.5, child: Icon(Icons.account_balance_wallet, size: 100, color: Colors.grey[400])),
        const SizedBox(height: 15),
        const Text("Your portfolio is empty", style: TextStyle(color: Colors.blueGrey, fontSize: 16)),
      ],
    );
  }

  Widget _buildFAB() {
    return FloatingActionButton.extended(
      elevation: 4,
      backgroundColor: const Color(0xFF0D47A1),
      onPressed: () async {
        final result = await Navigator.push(context, MaterialPageRoute(builder: (context) => const AddAssetScreen()));
        if (result == true) _loadData();
      },
      label: const Text("New Asset", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
      icon: const Icon(Icons.add_chart_rounded, color: Colors.white),
    );
  }

  // نافذة التعديل (نفس منطقك مع تحسين التصميم)
  void _showEditDialog(AssetModel asset) {
    final quantityController = TextEditingController(text: asset.quantity.toString());
    final priceController = TextEditingController(text: asset.purchasePrice.toString());

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text("Edit ${asset.symbol}"),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: quantityController, decoration: const InputDecoration(labelText: "Quantity"), keyboardType: TextInputType.number),
            TextField(controller: priceController, decoration: const InputDecoration(labelText: "Entry Price"), keyboardType: TextInputType.number),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text("Cancel")),
          ElevatedButton(
            onPressed: () async {
              await _assetService.updateAsset(asset.id!, {
                "symbol": asset.symbol,
                "asset_name": asset.assetName,
                "quantity": double.parse(quantityController.text),
                "purchase_price": double.parse(priceController.text),
              });
              Navigator.pop(context);
              _loadData();
            },
            child: const Text("Save"),
          ),
        ],
      ),
    );
  }
}

// مكون كرت الرصيد
class _BalanceCard extends StatelessWidget {
  final double balance;
  const _BalanceCard({required this.balance});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(25),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(30),
        gradient: const LinearGradient(begin: Alignment.topLeft, end: Alignment.bottomRight, colors: [Color(0xFF1E293B), Color(0xFF0F172A)]),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text("Net Worth", style: TextStyle(color: Colors.white60, fontSize: 14)),
              Container(padding: const EdgeInsets.all(5), decoration: BoxDecoration(color: Colors.greenAccent.withOpacity(0.1), borderRadius: BorderRadius.circular(8)), child: const Icon(Icons.trending_up, color: Colors.greenAccent, size: 16)),
            ],
          ),
          const SizedBox(height: 10),
          Text("\$${balance.toStringAsFixed(2)}", style: const TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}

// مكون عنصر القائمة مع خاصية السحب للحذف
class _AssetListItem extends StatelessWidget {
  final AssetModel asset;
  final VoidCallback onDelete;
  final VoidCallback onTap;

  const _AssetListItem({required this.asset, required this.onDelete, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Dismissible(
      key: Key(asset.id.toString()),
      direction: DismissDirection.endToStart,
      onDismissed: (_) => onDelete(),
      background: Container(
        margin: const EdgeInsets.only(bottom: 12),
        decoration: BoxDecoration(color: Colors.redAccent, borderRadius: BorderRadius.circular(15)),
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.only(right: 20),
        child: const Icon(Icons.delete_outline, color: Colors.white),
      ),
      child: Card(
        elevation: 0,
        margin: const EdgeInsets.only(bottom: 12),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15), side: BorderSide(color: Colors.grey[200]!)),
        child: ListTile(
          onTap: onTap,
          leading: CircleAvatar(backgroundColor: const Color(0xFF0D47A1).withOpacity(0.1), child: Text(asset.symbol[0], style: const TextStyle(color: Color(0xFF0D47A1), fontWeight: FontWeight.bold))),
          title: Text(asset.assetName, style: const TextStyle(fontWeight: FontWeight.bold)),
          subtitle: Text("${asset.quantity} units • \$${asset.purchasePrice}"),
          trailing: const Icon(Icons.chevron_right, color: Colors.grey),
        ),
      ),
    );
  }
}