import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'views/auth/login_screen.dart';

void main() {
  runApp(const InvestmentApp());
}

class InvestmentApp extends StatelessWidget {
  const InvestmentApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Portfolio',
      debugShowCheckedModeBanner: false, // Debug banner removed ✅
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF1E88E5),
          brightness: Brightness.light,
        ),
        // Professional English font
        textTheme: GoogleFonts.poppinsTextTheme(Theme.of(context).textTheme),
      ),
      home: LoginScreen(),
    );
  }
}