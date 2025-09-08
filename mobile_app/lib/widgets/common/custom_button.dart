import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../config/app_theme.dart';

class CustomButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final String text;
  final ButtonStyle? style;
  final double? width;
  final double? height;
  final Widget? icon;
  final bool isLoading;
  final bool isOutlined;
  final Color? backgroundColor;
  final Color? textColor;
  final double? borderRadius;
  final EdgeInsetsGeometry? padding;
  final TextStyle? textStyle;
  final bool isFullWidth;
  final bool isDisabled;

  const CustomButton({
    super.key,
    required this.onPressed,
    required this.text,
    this.style,
    this.width,
    this.height,
    this.icon,
    this.isLoading = false,
    this.isOutlined = false,
    this.backgroundColor,
    this.textColor,
    this.borderRadius,
    this.padding,
    this.textStyle,
    this.isFullWidth = false,
    this.isDisabled = false,
  });

  @override
  Widget build(BuildContext context) {
    final effectiveStyle = _getEffectiveStyle();
    final effectiveOnPressed = isDisabled ? null : (isLoading ? null : onPressed);

    Widget button;
    
    if (isOutlined) {
      button = OutlinedButton(
        onPressed: effectiveOnPressed,
        style: effectiveStyle,
        child: _buildButtonContent(),
      );
    } else {
      button = ElevatedButton(
        onPressed: effectiveOnPressed,
        style: effectiveStyle,
        child: _buildButtonContent(),
      );
    }

    if (isFullWidth) {
      button = SizedBox(
        width: double.infinity,
        child: button,
      );
    } else if (width != null) {
      button = SizedBox(
        width: width,
        child: button,
      );
    }

    return button;
  }

  ButtonStyle _getEffectiveStyle() {
    final baseStyle = style ?? _getDefaultStyle();
    
    return baseStyle.copyWith(
      backgroundColor: MaterialStateProperty.resolveWith((states) {
        if (isDisabled) {
          return AppTheme.disabledTextColor;
        }
        if (backgroundColor != null) {
          return backgroundColor;
        }
        return null;
      }),
      foregroundColor: MaterialStateProperty.resolveWith((states) {
        if (isDisabled) {
          return Colors.white;
        }
        if (textColor != null) {
          return textColor;
        }
        return null;
      }),
      padding: MaterialStateProperty.all(
        padding ?? const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
      ),
      shape: MaterialStateProperty.all(
        RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(borderRadius ?? 8),
        ),
      ),
    );
  }

  ButtonStyle _getDefaultStyle() {
    if (isOutlined) {
      return OutlinedButton.styleFrom(
        foregroundColor: AppTheme.primaryColor,
        side: const BorderSide(color: AppTheme.primaryColor, width: 1.5),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(borderRadius ?? 8),
        ),
        padding: padding ?? const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
      );
    } else {
      return ElevatedButton.styleFrom(
        backgroundColor: AppTheme.primaryColor,
        foregroundColor: Colors.white,
        elevation: 2,
        shadowColor: Colors.black26,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(borderRadius ?? 8),
        ),
        padding: padding ?? const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
      );
    }
  }

  Widget _buildButtonContent() {
    if (isLoading) {
      return SizedBox(
        height: height ?? 20,
        width: height ?? 20,
        child: CircularProgressIndicator(
          strokeWidth: 2,
          valueColor: AlwaysStoppedAnimation<Color>(
            isOutlined ? AppTheme.primaryColor : Colors.white,
          ),
        ),
      );
    }

    final content = <Widget>[];
    
    if (icon != null) {
      content.add(icon!);
      content.add(const SizedBox(width: 8));
    }
    
    content.add(
      Text(
        text,
        style: textStyle ?? GoogleFonts.poppins(
          fontSize: 16,
          fontWeight: FontWeight.w600,
        ),
      ),
    );

    return Row(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.center,
      children: content,
    );
  }
}

// Specialized button variants
class PrimaryButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final String text;
  final Widget? icon;
  final bool isLoading;
  final bool isFullWidth;
  final double? height;

  const PrimaryButton({
    super.key,
    required this.onPressed,
    required this.text,
    this.icon,
    this.isLoading = false,
    this.isFullWidth = false,
    this.height,
  });

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      onPressed: onPressed,
      text: text,
      icon: icon,
      isLoading: isLoading,
      isFullWidth: isFullWidth,
      height: height,
      style: AppTheme.primaryButtonStyle,
    );
  }
}

class SecondaryButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final String text;
  final Widget? icon;
  final bool isLoading;
  final bool isFullWidth;
  final double? height;

  const SecondaryButton({
    super.key,
    required this.onPressed,
    required this.text,
    this.icon,
    this.isLoading = false,
    this.isFullWidth = false,
    this.height,
  });

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      onPressed: onPressed,
      text: text,
      icon: icon,
      isLoading: isLoading,
      isFullWidth: isFullWidth,
      height: height,
      style: AppTheme.secondaryButtonStyle,
    );
  }
}

class DangerButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final String text;
  final Widget? icon;
  final bool isLoading;
  final bool isFullWidth;
  final double? height;

  const DangerButton({
    super.key,
    required this.onPressed,
    required this.text,
    this.icon,
    this.isLoading = false,
    this.isFullWidth = false,
    this.height,
  });

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      onPressed: onPressed,
      text: text,
      icon: icon,
      isLoading: isLoading,
      isFullWidth: isFullWidth,
      height: height,
      backgroundColor: AppTheme.errorColor,
      textColor: Colors.white,
    );
  }
}

class SuccessButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final String text;
  final Widget? icon;
  final bool isLoading;
  final bool isFullWidth;
  final double? height;

  const SuccessButton({
    super.key,
    required this.onPressed,
    required this.text,
    this.icon,
    this.isLoading = false,
    this.isFullWidth = false,
    this.height,
  });

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      onPressed: onPressed,
      text: text,
      icon: icon,
      isLoading: isLoading,
      isFullWidth: isFullWidth,
      height: height,
      backgroundColor: AppTheme.successColor,
      textColor: Colors.white,
    );
  }
}

class WarningButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final String text;
  final Widget? icon;
  final bool isLoading;
  final bool isFullWidth;
  final double? height;

  const WarningButton({
    super.key,
    required this.onPressed,
    required this.text,
    this.icon,
    this.isLoading = false,
    this.isFullWidth = false,
    this.height,
  });

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      onPressed: onPressed,
      text: text,
      icon: icon,
      isLoading: isLoading,
      isFullWidth: isFullWidth,
      height: height,
      backgroundColor: AppTheme.warningColor,
      textColor: Colors.white,
    );
  }
}

class InfoButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final String text;
  final Widget? icon;
  final bool isLoading;
  final bool isFullWidth;
  final double? height;

  const InfoButton({
    super.key,
    required this.onPressed,
    required this.text,
    this.icon,
    this.isLoading = false,
    this.isFullWidth = false,
    this.height,
  });

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      onPressed: onPressed,
      text: text,
      icon: icon,
      isLoading: isLoading,
      isFullWidth: isFullWidth,
      height: height,
      backgroundColor: AppTheme.infoColor,
      textColor: Colors.white,
    );
  }
}

class IconButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final IconData icon;
  final String? tooltip;
  final Color? backgroundColor;
  final Color? iconColor;
  final double? size;
  final bool isLoading;
  final bool isDisabled;

  const IconButton({
    super.key,
    required this.onPressed,
    required this.icon,
    this.tooltip,
    this.backgroundColor,
    this.iconColor,
    this.size,
    this.isLoading = false,
    this.isDisabled = false,
  });

  @override
  Widget build(BuildContext context) {
    return CustomButton(
      onPressed: onPressed,
      text: '',
      icon: Icon(
        icon,
        color: iconColor ?? AppTheme.primaryColor,
        size: size ?? 24,
      ),
      isLoading: isLoading,
      isDisabled: isDisabled,
      backgroundColor: backgroundColor ?? Colors.transparent,
      padding: const EdgeInsets.all(12),
      borderRadius: 50,
      width: (size ?? 24) + 24,
      height: (size ?? 24) + 24,
    );
  }
}

