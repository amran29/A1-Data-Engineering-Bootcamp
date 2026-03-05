import 'package:flutter/material.dart';
import '../../services/auth_service.dart';
import '../portfolio/home_screen.dart'; // تأكد من المسار الصحيح

class SignupScreen extends StatefulWidget {
  const SignupScreen({super.key}); // إضافة الـ key و const

  @override
  State<SignupScreen> createState() => _SignupScreenState();
}

class _SignupScreenState extends State<SignupScreen> {
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final AuthService _authService = AuthService(); // تعريف الخدمة

  bool _isLoading = false;

  // دالة التسجيل الأساسية
  Future<void> _handleSignup() async {
    // 1. التحقق الأولي من الحقول
    if (_nameController.text.isEmpty || _emailController.text.isEmpty || _passwordController.text.isEmpty) {
      _showErrorSnackBar("Please fill all fields");
      return;
    }

    setState(() => _isLoading = true);

    try {
      // 2. استدعاء AuthService المحدث
      final success = await _authService.register(
        _nameController.text.trim(),
        _emailController.text.trim(),
        _passwordController.text.trim(),
      );

      if (success && mounted) {
        // 3. في حال النجاح، محاولة تسجيل الدخول تلقائياً أو التوجه لشاشة الدخول
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Account created successfully!"), backgroundColor: Colors.green),
        );
        Navigator.pop(context); // العودة لصفحة الدخول
      }
    } catch (e) {
      // هنا سيتم التقاط رسالة الخطأ النصية التي أصلحناها في AuthService
      if (mounted) _showErrorSnackBar(e.toString());
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  void _showErrorSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.redAccent,
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  @override
  void dispose() {
    // تنظيف الذاكرة (مهم جداً)
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF1E88E5), // توحيد اللون الخلفي
      appBar: AppBar(
        backgroundColor: Colors.transparent, // جعل الـ AppBar شفاف
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF1E88E5), Color(0xFF1565C0)],
          ),
        ),
        child: Column(
          children: [
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 20),
              child: Text("Create Account",
                  style: TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold)),
            ),
            Expanded(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 40),
                decoration: const BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.only(topLeft: Radius.circular(60)),
                ),
                child: SingleChildScrollView(
                  child: Column(
                    children: [
                      _buildInput("Full Name", Icons.person_outline, _nameController),
                      const SizedBox(height: 20),
                      _buildInput("Email Address", Icons.email_outlined, _emailController),
                      const SizedBox(height: 20),
                      _buildInput("Password", Icons.lock_outline, _passwordController, isPass: true),
                      const SizedBox(height: 40),
                      _isLoading
                          ? const CircularProgressIndicator(color: Color(0xFF1565C0))
                          : SizedBox(
                        width: double.infinity,
                        height: 55,
                        child: ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF1565C0),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                            elevation: 5,
                          ),
                          onPressed: _handleSignup, // ربط الدالة هنا
                          child: const Text("Sign Up", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildInput(String hint, IconData icon, TextEditingController controller, {bool isPass = false}) {
    return TextField(
      controller: controller,
      obscureText: isPass,
      style: const TextStyle(color: Colors.black87),
      decoration: InputDecoration(
        prefixIcon: Icon(icon, color: const Color(0xFF1E88E5)),
        hintText: hint,
        hintStyle: TextStyle(color: Colors.grey[400]),
        filled: true,
        fillColor: Colors.grey[100],
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: BorderSide(color: Colors.grey[200]!),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: const BorderSide(color: Color(0xFF1E88E5)),
        ),
      ),
    );
  }
}