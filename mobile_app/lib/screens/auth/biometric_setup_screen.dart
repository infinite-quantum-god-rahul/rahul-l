import 'package:flutter/material.dart';
import 'package:local_auth/local_auth.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:get/get.dart';
import '../../config/app_routes.dart';
import '../../providers/auth_provider.dart';
import '../../widgets/common/custom_button.dart';
import '../../widgets/common/custom_text_field.dart';
import '../../widgets/common/loading_overlay.dart';
import '../../config/app_theme.dart';
import '../../utils/constants.dart';

class BiometricSetupScreen extends StatefulWidget {
  const BiometricSetupScreen({Key? key}) : super(key: key);

  @override
  State<BiometricSetupScreen> createState() => _BiometricSetupScreenState();
}

class _BiometricSetupScreenState extends State<BiometricSetupScreen>
    with TickerProviderStateMixin {
  final _formKey = GlobalKey<FormState>();
  final _pinController = TextEditingController();
  final _confirmPinController = TextEditingController();
  
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;
  
  bool _isBiometricAvailable = false;
  bool _isBiometricEnabled = false;
  bool _isLoading = false;
  bool _showPinSetup = false;
  bool _pinError = false;
  String _errorMessage = '';
  
  final LocalAuthentication _localAuth = LocalAuthentication();
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();

  @override
  void initState() {
    super.initState();
    _initializeAnimations();
    _checkBiometricAvailability();
  }

  @override
  void dispose() {
    _animationController.dispose();
    _pinController.dispose();
    _confirmPinController.dispose();
    super.dispose();
  }

  void _initializeAnimations() {
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    
    _fadeAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeInOut,
    ));
    
    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 0.3),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeOutCubic,
    ));
    
    _animationController.forward();
  }

  Future<void> _checkBiometricAvailability() async {
    try {
      setState(() {
        _isLoading = true;
      });
      
      // Check if biometric authentication is available
      final isAvailable = await _localAuth.canCheckBiometrics;
      final isDeviceSupported = await _localAuth.isDeviceSupported();
      
      if (isAvailable && isDeviceSupported) {
        final availableBiometrics = await _localAuth.getAvailableBiometrics();
        
        setState(() {
          _isBiometricAvailable = availableBiometrics.isNotEmpty;
          _isLoading = false;
        });
        
        // Check if biometric is already enabled
        if (_isBiometricAvailable) {
          await _checkBiometricStatus();
        }
      } else {
        setState(() {
          _isBiometricAvailable = false;
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        _isBiometricAvailable = false;
        _isLoading = false;
        _errorMessage = 'Failed to check biometric availability: $e';
      });
    }
  }

  Future<void> _checkBiometricStatus() async {
    try {
      final isEnabled = await _secureStorage.read(
        key: AppConstants.biometricEnabledKey,
      );
      
      setState(() {
        _isBiometricEnabled = isEnabled == 'true';
      });
    } catch (e) {
      // Ignore errors
    }
  }

  Future<void> _setupBiometric() async {
    try {
      setState(() {
        _isLoading = true;
        _errorMessage = '';
      });
      
      // Authenticate with biometric
      final isAuthenticated = await _localAuth.authenticate(
        localizedReason: 'Please authenticate to enable biometric login',
        options: const AuthenticationOptions(
          stickyAuth: true,
          biometricOnly: true,
        ),
      );
      
      if (isAuthenticated) {
        // Enable biometric
        await _secureStorage.write(
          key: AppConstants.biometricEnabledKey,
          value: 'true',
        );
        
        setState(() {
          _isBiometricEnabled = true;
          _isLoading = false;
        });
        
        // Navigate to main app
        Get.offAllNamed(AppRoutes.mainNavigation);
      } else {
        setState(() {
          _isLoading = false;
          _errorMessage = 'Biometric authentication failed';
        });
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
        _errorMessage = 'Failed to setup biometric: $e';
      });
    }
  }

  Future<void> _setupPin() async {
    if (!_formKey.currentState!.validate()) return;
    
    if (_pinController.text != _confirmPinController.text) {
      setState(() {
        _pinError = true;
        _errorMessage = 'PINs do not match';
      });
      return;
    }
    
    try {
      setState(() {
        _isLoading = true;
        _errorMessage = '';
        _pinError = false;
      });
      
      // Store PIN securely
      await _secureStorage.write(
        key: AppConstants.pinKey,
        value: _pinController.text,
      );
      
      // Enable PIN authentication
      await _secureStorage.write(
        key: AppConstants.pinEnabledKey,
        value: 'true',
      );
      
      setState(() {
        _isLoading = false;
      });
      
      // Navigate to main app
      Get.offAllNamed(AppRoutes.mainNavigation);
    } catch (e) {
      setState(() {
        _isLoading = false;
        _errorMessage = 'Failed to setup PIN: $e';
      });
    }
  }

  void _skipSetup() {
    Get.offAllNamed(AppRoutes.mainNavigation);
  }

  void _showPinSetupForm() {
    setState(() {
      _showPinSetup = true;
      _errorMessage = '';
      _pinError = false;
    });
  }

  void _hidePinSetupForm() {
    setState(() {
      _showPinSetup = false;
      _errorMessage = '';
      _pinError = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: LoadingOverlay(
        isLoading: _isLoading,
        child: Container(
          decoration: BoxDecoration(
            gradient: AppTheme.primaryGradient,
          ),
          child: SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(AppConfig.defaultPadding),
              child: Column(
                children: [
                  // Header
                  Expanded(
                    flex: 2,
                    child: FadeTransition(
                      opacity: _fadeAnimation,
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.fingerprint,
                            size: 80,
                            color: Colors.white,
                          ),
                          const SizedBox(height: 24),
                          Text(
                            'Secure Your Account',
                            style: AppTheme.lightTheme.textTheme.headlineMedium?.copyWith(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 16),
                          Text(
                            'Choose how you want to access your account securely',
                            style: AppTheme.lightTheme.textTheme.bodyLarge?.copyWith(
                              color: Colors.white.withOpacity(0.9),
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    ),
                  ),
                  
                  // Content
                  Expanded(
                    flex: 3,
                    child: SlideTransition(
                      position: _slideAnimation,
                      child: FadeTransition(
                        opacity: _fadeAnimation,
                        child: Container(
                          width: double.infinity,
                          padding: const EdgeInsets.all(24),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(20),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withOpacity(0.1),
                                blurRadius: 20,
                                offset: const Offset(0, 10),
                              ),
                            ],
                          ),
                          child: _showPinSetup ? _buildPinSetupForm() : _buildBiometricOptions(),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildBiometricOptions() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        // Biometric Option
        if (_isBiometricAvailable) ...[
          _buildOptionCard(
            icon: Icons.fingerprint,
            title: 'Use Biometric',
            subtitle: 'Login with fingerprint or face recognition',
            onTap: _setupBiometric,
            isEnabled: !_isBiometricEnabled,
          ),
          const SizedBox(height: 16),
        ],
        
        // PIN Option
        _buildOptionCard(
          icon: Icons.pin,
          title: 'Use PIN',
          subtitle: 'Create a secure 4-digit PIN',
          onTap: _showPinSetupForm,
          isEnabled: true,
        ),
        
        const SizedBox(height: 24),
        
        // Skip Option
        TextButton(
          onPressed: _skipSetup,
          child: Text(
            'Skip for now',
            style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
              color: AppTheme.textSecondaryColor,
            ),
          ),
        ),
        
        // Error Message
        if (_errorMessage.isNotEmpty) ...[
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppTheme.errorColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(
                color: AppTheme.errorColor.withOpacity(0.3),
              ),
            ),
            child: Row(
              children: [
                Icon(
                  Icons.error_outline,
                  color: AppTheme.errorColor,
                  size: 20,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    _errorMessage,
                    style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                      color: AppTheme.errorColor,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildPinSetupForm() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        // Header
        Row(
          children: [
            IconButton(
              onPressed: _hidePinSetupForm,
              icon: const Icon(Icons.arrow_back),
              color: AppTheme.textPrimaryColor,
            ),
            Expanded(
              child: Text(
                'Create PIN',
                style: AppTheme.lightTheme.textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),
            ),
            const SizedBox(width: 48), // Balance the back button
          ],
        ),
        
        const SizedBox(height: 24),
        
        // PIN Form
        Form(
          key: _formKey,
          child: Column(
            children: [
              CustomTextField(
                controller: _pinController,
                labelText: 'Enter 4-digit PIN',
                hintText: '1234',
                keyboardType: TextInputType.number,
                obscureText: true,
                maxLength: 4,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter a PIN';
                  }
                  if (value.length != 4) {
                    return 'PIN must be 4 digits';
                  }
                  if (!RegExp(r'^[0-9]+$').hasMatch(value)) {
                    return 'PIN must contain only numbers';
                  }
                  return null;
                },
                onChanged: (value) {
                  if (_pinError) {
                    setState(() {
                      _pinError = false;
                      _errorMessage = '';
                    });
                  }
                },
              ),
              
              const SizedBox(height: 16),
              
              CustomTextField(
                controller: _confirmPinController,
                labelText: 'Confirm PIN',
                hintText: '1234',
                keyboardType: TextInputType.number,
                obscureText: true,
                maxLength: 4,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please confirm your PIN';
                  }
                  if (value != _pinController.text) {
                    return 'PINs do not match';
                  }
                  return null;
                },
                onChanged: (value) {
                  if (_pinError) {
                    setState(() {
                      _pinError = false;
                      _errorMessage = '';
                    });
                  }
                },
              ),
            ],
          ),
        ),
        
        const SizedBox(height: 24),
        
        // Setup Button
        CustomButton(
          onPressed: _setupPin,
          text: 'Setup PIN',
          isFullWidth: true,
          style: CustomButtonStyle.primary,
        ),
        
        const SizedBox(height: 16),
        
        // Error Message
        if (_errorMessage.isNotEmpty) ...[
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppTheme.errorColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(
                color: AppTheme.errorColor.withOpacity(0.3),
              ),
            ),
            child: Row(
              children: [
                Icon(
                  Icons.error_outline,
                  color: AppTheme.errorColor,
                  size: 20,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    _errorMessage,
                    style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                      color: AppTheme.errorColor,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildOptionCard({
    required IconData icon,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
    required bool isEnabled,
  }) {
    return Container(
      width: double.infinity,
      child: Card(
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        child: InkWell(
          onTap: isEnabled ? onTap : null,
          borderRadius: BorderRadius.circular(12),
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: isEnabled 
                        ? AppTheme.primaryColor.withOpacity(0.1)
                        : AppTheme.textSecondaryColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(
                    icon,
                    size: 28,
                    color: isEnabled 
                        ? AppTheme.primaryColor
                        : AppTheme.textSecondaryColor,
                  ),
                ),
                
                const SizedBox(width: 16),
                
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: AppTheme.lightTheme.textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                          color: isEnabled 
                              ? AppTheme.textPrimaryColor
                              : AppTheme.textSecondaryColor,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        subtitle,
                        style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                          color: isEnabled 
                              ? AppTheme.textSecondaryColor
                              : AppTheme.textSecondaryColor.withOpacity(0.6),
                        ),
                      ),
                    ],
                  ),
                ),
                
                Icon(
                  Icons.arrow_forward_ios,
                  size: 16,
                  color: isEnabled 
                      ? AppTheme.textSecondaryColor
                      : AppTheme.textSecondaryColor.withOpacity(0.3),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

