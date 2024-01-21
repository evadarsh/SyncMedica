import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:sync_medica/login_page.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen
({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
void initState(){
  super.initState();
  Future.delayed(const Duration(seconds: 5), () {
    Navigator.of(context).pushReplacement(MaterialPageRoute(builder: (context) => const LoginPage()));
  });
}
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Lottie.asset(
          'assets/Splash-Animation.json',
          fit: BoxFit.fill,
        ),
      ),
    );
  }
}