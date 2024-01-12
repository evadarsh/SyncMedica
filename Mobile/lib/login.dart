// ignore_for_file: unnecessary_const
import 'package:flutter/material.dart';

class Login extends StatefulWidget {
  const Login({super.key});

  @override
  State<Login> createState() => _LoginState();
}

class _LoginState extends State<Login> {
  final TextEditingController _emailcontroller = TextEditingController();
  final TextEditingController _passwordcontroller = TextEditingController();
  bool _obscureText = true;
  void login() {
    print({_emailcontroller.text});
    print({_passwordcontroller.text});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Container(
      padding: const EdgeInsets.all(20),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Center(
              child: Text(
            'Sync Medica',
            style: const TextStyle(
              fontSize: 30,
              fontWeight: FontWeight.bold,
              color: Color.fromRGBO(10, 218, 255, 1),
            ),
          )),
          const SizedBox(
            height: 10,
          ),
          TextFormField(
            controller: _emailcontroller,
            decoration: InputDecoration(
              hintText: 'Email',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10),
              ),
            ),
          ),
          const SizedBox(
            height: 10,
          ),
          TextFormField(
            obscureText: _obscureText,
            controller: _passwordcontroller,
            decoration: InputDecoration(
              suffixIcon: InkWell(
                child: Icon(Icons.remove_red_eye),onTap: () {
                  setState(() {
                    _obscureText =!_obscureText;
                  });
                },
              ),
              hintText: 'Password',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: ElevatedButton(
                onPressed: () {
                  login();
                },
                child: const Text('Login')),
          ),
          Center(child: ElevatedButton(onPressed: () {}, child: const Text('Sign Up'))),
          GestureDetector(
              onTap: () {
                print('Forget Password....................');
              },
              child: const Text('Forget Password?')),
        ],
      ),
    ));
  }
}
