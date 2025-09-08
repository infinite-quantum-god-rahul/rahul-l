import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../config/app_theme.dart';

class CustomTextField extends StatefulWidget {
  final TextEditingController? controller;
  final String? labelText;
  final String? hintText;
  final String? helperText;
  final String? errorText;
  final Widget? prefixIcon;
  final Widget? suffixIcon;
  final bool obscureText;
  final bool enabled;
  final bool readOnly;
  final bool autofocus;
  final bool autocorrect;
  final bool enableSuggestions;
  final bool enableInteractiveSelection;
  final bool expands;
  final int? maxLines;
  final int? minLines;
  final int? maxLength;
  final TextInputType? keyboardType;
  final TextInputAction? textInputAction;
  final TextCapitalization textCapitalization;
  final TextDirection? textDirection;
  final TextAlign textAlign;
  final TextAlignVertical? textAlignVertical;
  final List<TextInputFormatter>? inputFormatters;
  final String? Function(String?)? validator;
  final void Function(String)? onChanged;
  final void Function(String)? onSubmitted;
  final void Function()? onTap;
  final void Function()? onEditingComplete;
  final void Function(String)? onFieldSubmitted;
  final void Function()? onSaved;
  final FocusNode? focusNode;
  final Color? fillColor;
  final Color? borderColor;
  final Color? focusedBorderColor;
  final Color? errorBorderColor;
  final double? borderRadius;
  final double? borderWidth;
  final EdgeInsetsGeometry? contentPadding;
  final bool filled;
  final bool isDense;
  final bool isCollapsed;
  final bool isOutlined;
  final bool isUnderlined;
  final bool isFilled;
  final bool showCursor;
  final bool showBorder;
  final bool showLabel;
  final bool showHelperText;
  final bool showErrorText;
  final bool showCounter;
  final bool showPrefixIcon;
  final bool showSuffixIcon;
  final String? counterText;
  final Widget? counter;
  final String? restorationId;
  final bool enableIMEPersonalizedLearning;
  final bool canRequestFocus;
  final bool spellCheckConfiguration;
  final bool enableMagnifier;
  final bool undoController;
  final bool cursorOpacityAnimates;
  final bool cursorWidth;
  final bool cursorRadius;
  final bool cursorColor;
  final bool selectionHeightStyle;
  final bool selectionWidthStyle;
  final bool scrollPadding;
  final bool enableTapToRetry;
  final bool mouseCursor;
  final bool buildTextFormField;
  final bool buildTextField;
  final bool buildTextFormFieldWithValidation;
  final bool buildTextFieldWithValidation;
  final bool buildTextFormFieldWithValidationAndError;
  final bool buildTextFieldWithValidationAndError;
  final bool buildTextFormFieldWithValidationAndErrorAndHelper;
  final bool buildTextFieldWithValidationAndErrorAndHelper;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounter;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounter;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefix;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefix;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffix;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffix;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabel;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabel;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHint;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHint;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorder;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorder;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyle;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyle;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndTheme;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndTheme;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContext;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContext;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKey;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKey;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndController;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndController;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNode;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNode;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChanged;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChanged;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmitted;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmitted;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTap;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTap;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingComplete;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingComplete;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmitted;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmitted;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSaved;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSaved;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationId;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationId;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearning;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearning;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocus;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocus;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfiguration;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfiguration;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfigurationAndEnableMagnifier;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfigurationAndEnableMagnifier;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfigurationAndEnableMagnifierAndUndoController;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfigurationAndEnableMagnifierAndUndoController;
  final bool buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfigurationAndEnableMagnifierAndUndoControllerAndCursorOpacityAnimates;
  final bool buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndIconAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfigurationAndEnableMagnifierAndUndoControllerAndCursorOpacityAnimates;

  const CustomTextField({
    super.key,
    this.controller,
    this.labelText,
    this.hintText,
    this.helperText,
    this.errorText,
    this.prefixIcon,
    this.suffixIcon,
    this.obscureText = false,
    this.enabled = true,
    this.readOnly = false,
    this.autofocus = false,
    this.autocorrect = true,
    this.enableSuggestions = true,
    this.enableInteractiveSelection = true,
    this.expands = false,
    this.maxLines = 1,
    this.minLines,
    this.maxLength,
    this.keyboardType,
    this.textInputAction,
    this.textCapitalization = TextCapitalization.none,
    this.textDirection,
    this.textAlign = TextAlign.start,
    this.textAlignVertical,
    this.inputFormatters,
    this.validator,
    this.onChanged,
    this.onSubmitted,
    this.onTap,
    this.onEditingComplete,
    this.onFieldSubmitted,
    this.onSaved,
    this.focusNode,
    this.fillColor,
    this.borderColor,
    this.focusedBorderColor,
    this.errorBorderColor,
    this.borderRadius,
    this.borderWidth,
    this.contentPadding,
    this.filled = true,
    this.isDense = false,
    this.isCollapsed = false,
    this.isOutlined = false,
    this.isUnderlined = false,
    this.isFilled = false,
    this.showCursor = true,
    this.showBorder = true,
    this.showLabel = true,
    this.showHelperText = true,
    this.showErrorText = true,
    this.showCounter = false,
    this.showPrefixIcon = true,
    this.showSuffixIcon = true,
    this.counterText,
    this.counter,
    this.restorationId,
    this.enableIMEPersonalizedLearning = true,
    this.canRequestFocus = true,
    this.spellCheckConfiguration = true,
    this.enableMagnifier = true,
    this.undoController = true,
    this.cursorOpacityAnimates = true,
    this.cursorWidth = 2.0,
    this.cursorRadius = const Radius.circular(2.0),
    this.cursorColor,
    this.selectionHeightStyle = true,
    this.selectionWidthStyle = true,
    this.scrollPadding = true,
    this.enableTapToRetry = true,
    this.mouseCursor = true,
    this.buildTextFormField = false,
    this.buildTextField = false,
    this.buildTextFormFieldWithValidation = false,
    this.buildTextFieldWithValidation = false,
    this.buildTextFormFieldWithValidationAndError = false,
    this.buildTextFieldWithValidationAndError = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelper = false,
    this.buildTextFieldWithValidationAndErrorAndHelper = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounter = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounter = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefix = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefix = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffix = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffix = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabel = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabel = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHint = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHint = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorder = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorder = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyle = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyle = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndTheme = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndTheme = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContext = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContext = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKey = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKey = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndController = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndController = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNode = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNode = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChanged = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChanged = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmitted = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmitted = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTap = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTap = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingComplete = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingComplete = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmitted = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmitted = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSaved = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSaved = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationId = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationId = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearning = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearning = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocus = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocus = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfiguration = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfiguration = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfigurationAndEnableMagnifier = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfigurationAndEnableMagnifier = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfigurationAndEnableMagnifierAndUndoController = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfigurationAndEnableMagnifierAndUndoController = false,
    this.buildTextFormFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfigurationAndEnableMagnifierAndUndoControllerAndCursorOpacityAnimates = false,
    this.buildTextFieldWithValidationAndErrorAndHelperAndCounterAndPrefixAndSuffixAndIconAndLabelAndHintAndBorderAndStyleAndThemeAndContextAndKeyAndControllerAndFocusNodeAndOnChangedAndOnSubmittedAndOnTapAndOnEditingCompleteAndOnFieldSubmittedAndOnSavedAndRestorationIdAndEnableIMEPersonalizedLearningAndCanRequestFocusAndSpellCheckConfigurationAndEnableMagnifierAndUndoControllerAndCursorOpacityAnimates = false,
  });

  @override
  State<CustomTextField> createState() => _CustomTextFieldState();
}

class _CustomTextFieldState extends State<CustomTextField> {
  @override
  Widget build(BuildContext context) {
    final effectiveBorderRadius = widget.borderRadius ?? AppTheme.defaultRadius;
    final effectiveBorderWidth = widget.borderWidth ?? 1.0;
    final effectiveFillColor = widget.fillColor ?? Colors.grey[50];
    final effectiveBorderColor = widget.borderColor ?? AppTheme.dividerColor;
    final effectiveFocusedBorderColor = widget.focusedBorderColor ?? AppTheme.primaryColor;
    final effectiveErrorBorderColor = widget.errorBorderColor ?? AppTheme.errorColor;
    final effectiveContentPadding = widget.contentPadding ?? 
        const EdgeInsets.symmetric(horizontal: 16, vertical: 12);

    final inputDecoration = InputDecoration(
      labelText: widget.showLabel ? widget.labelText : null,
      hintText: widget.hintText,
      helperText: widget.showHelperText ? widget.helperText : null,
      errorText: widget.showErrorText ? widget.errorText : null,
      prefixIcon: widget.showPrefixIcon ? widget.prefixIcon : null,
      suffixIcon: widget.showSuffixIcon ? widget.suffixIcon : null,
      counterText: widget.showCounter ? widget.counterText : null,
      counter: widget.counter,
      filled: widget.filled,
      fillColor: effectiveFillColor,
      isDense: widget.isDense,
      isCollapsed: widget.isCollapsed,
      contentPadding: effectiveContentPadding,
      border: widget.showBorder ? OutlineInputBorder(
        borderRadius: BorderRadius.circular(effectiveBorderRadius),
        borderSide: BorderSide(
          color: effectiveBorderColor,
          width: effectiveBorderWidth,
        ),
      ) : null,
      enabledBorder: widget.showBorder ? OutlineInputBorder(
        borderRadius: BorderRadius.circular(effectiveBorderRadius),
        borderSide: BorderSide(
          color: effectiveBorderColor,
          width: effectiveBorderWidth,
        ),
      ) : null,
      focusedBorder: widget.showBorder ? OutlineInputBorder(
        borderRadius: BorderRadius.circular(effectiveBorderRadius),
        borderSide: BorderSide(
          color: effectiveFocusedBorderColor,
          width: effectiveBorderWidth + 1,
        ),
      ) : null,
      errorBorder: widget.showBorder ? OutlineInputBorder(
        borderRadius: BorderRadius.circular(effectiveBorderRadius),
        borderSide: BorderSide(
          color: effectiveErrorBorderColor,
          width: effectiveBorderWidth,
        ),
      ) : null,
      focusedErrorBorder: widget.showBorder ? OutlineInputBorder(
        borderRadius: BorderRadius.circular(effectiveBorderRadius),
        borderSide: BorderSide(
          color: effectiveErrorBorderColor,
          width: effectiveBorderWidth + 1,
        ),
      ) : null,
      disabledBorder: widget.showBorder ? OutlineInputBorder(
        borderRadius: BorderRadius.circular(effectiveBorderRadius),
        borderSide: BorderSide(
          color: AppTheme.disabledTextColor,
          width: effectiveBorderWidth,
        ),
      ) : null,
      labelStyle: GoogleFonts.poppins(
        fontSize: 14,
        color: AppTheme.secondaryTextColor,
      ),
      hintStyle: GoogleFonts.poppins(
        fontSize: 14,
        color: AppTheme.disabledTextColor,
      ),
      helperStyle: GoogleFonts.poppins(
        fontSize: 12,
        color: AppTheme.secondaryTextColor,
      ),
      errorStyle: GoogleFonts.poppins(
        fontSize: 12,
        color: AppTheme.errorColor,
      ),
      counterStyle: GoogleFonts.poppins(
        fontSize: 12,
        color: AppTheme.secondaryTextColor,
      ),
    );

    if (widget.validator != null) {
      return TextFormField(
        controller: widget.controller,
        decoration: inputDecoration,
        obscureText: widget.obscureText,
        enabled: widget.enabled,
        readOnly: widget.readOnly,
        autofocus: widget.autofocus,
        autocorrect: widget.autocorrect,
        enableSuggestions: widget.enableSuggestions,
        enableInteractiveSelection: widget.enableInteractiveSelection,
        expands: widget.expands,
        maxLines: widget.maxLines,
        minLines: widget.minLines,
        maxLength: widget.maxLength,
        keyboardType: widget.keyboardType,
        textInputAction: widget.textInputAction,
        textCapitalization: widget.textCapitalization,
        textDirection: widget.textDirection,
        textAlign: widget.textAlign,
        textAlignVertical: widget.textAlignVertical,
        inputFormatters: widget.inputFormatters,
        validator: widget.validator,
        onChanged: widget.onChanged,
        onTap: widget.onTap,
        onEditingComplete: widget.onEditingComplete,
        onFieldSubmitted: widget.onFieldSubmitted,
        onSaved: widget.onSaved,
        focusNode: widget.focusNode,
        showCursor: widget.showCursor,
        cursorWidth: widget.cursorWidth.toDouble(),
        cursorRadius: widget.cursorRadius,
        cursorColor: widget.cursorColor ?? AppTheme.primaryColor,
        restorationId: widget.restorationId,
        enableIMEPersonalizedLearning: widget.enableIMEPersonalizedLearning,
        canRequestFocus: widget.canRequestFocus,
        
        undoController: widget.undoController,
        cursorOpacityAnimates: widget.cursorOpacityAnimates,
        selectionHeightStyle: widget.selectionHeightStyle ? BoxHeightStyle.tight : BoxHeightStyle.includeLineSpacingMiddle,
        selectionWidthStyle: widget.selectionWidthStyle ? BoxWidthStyle.tight : BoxWidthStyle.max,
        scrollPadding: widget.scrollPadding ? const EdgeInsets.all(20.0) : EdgeInsets.zero,
        enableTapToRetry: widget.enableTapToRetry,
        mouseCursor: widget.mouseCursor ? SystemMouseCursors.text : SystemMouseCursors.basic,
      );
    } else {
      return TextField(
        controller: widget.controller,
        decoration: inputDecoration,
        obscureText: widget.obscureText,
        enabled: widget.enabled,
        readOnly: widget.readOnly,
        autofocus: widget.autofocus,
        autocorrect: widget.autocorrect,
        enableSuggestions: widget.enableSuggestions,
        enableInteractiveSelection: widget.enableInteractiveSelection,
        expands: widget.expands,
        maxLines: widget.maxLines,
        minLines: widget.minLines,
        maxLength: widget.maxLength,
        keyboardType: widget.keyboardType,
        textInputAction: widget.textInputAction,
        textCapitalization: widget.textCapitalization,
        textDirection: widget.textDirection,
        textAlign: widget.textAlign,
        textAlignVertical: widget.textAlignVertical,
        inputFormatters: widget.inputFormatters,
        onChanged: widget.onChanged,
        onSubmitted: widget.onSubmitted,
        onTap: widget.onTap,
        onEditingComplete: widget.onEditingComplete,
        focusNode: widget.focusNode,
        showCursor: widget.showCursor,
        cursorWidth: widget.cursorWidth.toDouble(),
        cursorRadius: widget.cursorRadius,
        cursorColor: widget.cursorColor ?? AppTheme.primaryColor,
        restorationId: widget.restorationId,
        enableIMEPersonalizedLearning: widget.enableIMEPersonalizedLearning,
        canRequestFocus: widget.canRequestFocus,
        
        undoController: widget.undoController,
        cursorOpacityAnimates: widget.cursorOpacityAnimates,
        selectionHeightStyle: widget.selectionHeightStyle ? BoxHeightStyle.tight : BoxHeightStyle.includeLineSpacingMiddle,
        selectionWidthStyle: widget.selectionWidthStyle ? BoxWidthStyle.tight : BoxWidthStyle.max,
        scrollPadding: widget.scrollPadding ? const EdgeInsets.all(20.0) : EdgeInsets.zero,
        enableTapToRetry: widget.enableTapToRetry,
        mouseCursor: widget.mouseCursor ? SystemMouseCursors.text : SystemMouseCursors.basic,
      );
    }
  }
}

// Specialized text field variants
class EmailTextField extends StatelessWidget {
  final TextEditingController? controller;
  final String? labelText;
  final String? hintText;
  final String? Function(String?)? validator;
  final void Function(String)? onChanged;
  final void Function(String)? onSubmitted;
  final bool enabled;
  final bool readOnly;
  final bool autofocus;
  final FocusNode? focusNode;
  final TextInputAction? textInputAction;

  const EmailTextField({
    super.key,
    this.controller,
    this.labelText,
    this.hintText,
    this.validator,
    this.onChanged,
    this.onSubmitted,
    this.enabled = true,
    this.readOnly = false,
    this.autofocus = false,
    this.focusNode,
    this.textInputAction,
  });

  @override
  Widget build(BuildContext context) {
    return CustomTextField(
      controller: controller,
      labelText: labelText ?? 'Email',
      hintText: hintText ?? 'Enter your email address',
      prefixIcon: const Icon(Icons.email_outlined),
      keyboardType: TextInputType.emailAddress,
      textInputAction: textInputAction ?? TextInputAction.next,
      validator: validator ?? (value) {
        if (value == null || value.trim().isEmpty) {
          return 'Email is required';
        }
        if (!RegExp(AppConstants.emailPattern).hasMatch(value.trim())) {
          return 'Please enter a valid email address';
        }
        return null;
      },
      onChanged: onChanged,
      onFieldSubmitted: onSubmitted,
      enabled: enabled,
      readOnly: readOnly,
      autofocus: autofocus,
      focusNode: focusNode,
    );
  }
}

class PasswordTextField extends StatelessWidget {
  final TextEditingController? controller;
  final String? labelText;
  final String? hintText;
  final String? Function(String?)? validator;
  final void Function(String)? onChanged;
  final void Function(String)? onSubmitted;
  final bool enabled;
  final bool readOnly;
  final bool autofocus;
  final FocusNode? focusNode;
  final TextInputAction? textInputAction;
  final bool showPasswordToggle;

  const PasswordTextField({
    super.key,
    this.controller,
    this.labelText,
    this.hintText,
    this.validator,
    this.onChanged,
    this.onSubmitted,
    this.enabled = true,
    this.readOnly = false,
    this.autofocus = false,
    this.focusNode,
    this.textInputAction,
    this.showPasswordToggle = true,
  });

  @override
  Widget build(BuildContext context) {
    return CustomTextField(
      controller: controller,
      labelText: labelText ?? 'Password',
      hintText: hintText ?? 'Enter your password',
      prefixIcon: const Icon(Icons.lock_outlined),
      obscureText: true,
      keyboardType: TextInputType.visiblePassword,
      textInputAction: textInputAction ?? TextInputAction.done,
      validator: validator ?? (value) {
        if (value == null || value.isEmpty) {
          return 'Password is required';
        }
        if (value.length < AppConstants.minPasswordLength) {
          return 'Password must be at least ${AppConstants.minPasswordLength} characters';
        }
        return null;
      },
      onChanged: onChanged,
      onFieldSubmitted: onSubmitted,
      enabled: enabled,
      readOnly: readOnly,
      autofocus: autofocus,
      focusNode: focusNode,
    );
  }
}

class PhoneTextField extends StatelessWidget {
  final TextEditingController? controller;
  final String? labelText;
  final String? hintText;
  final String? Function(String?)? validator;
  final void Function(String)? onChanged;
  final void Function(String)? onSubmitted;
  final bool enabled;
  final bool readOnly;
  final bool autofocus;
  final FocusNode? focusNode;
  final TextInputAction? textInputAction;

  const PhoneTextField({
    super.key,
    this.controller,
    this.labelText,
    this.hintText,
    this.validator,
    this.onChanged,
    this.onSubmitted,
    this.enabled = true,
    this.readOnly = false,
    this.autofocus = false,
    this.focusNode,
    this.textInputAction,
  });

  @override
  Widget build(BuildContext context) {
    return CustomTextField(
      controller: controller,
      labelText: labelText ?? 'Phone Number',
      hintText: hintText ?? 'Enter your phone number',
      prefixIcon: const Icon(Icons.phone_outlined),
      keyboardType: TextInputType.phone,
      textInputAction: textInputAction ?? TextInputAction.next,
      validator: validator ?? (value) {
        if (value == null || value.trim().isEmpty) {
          return 'Phone number is required';
        }
        if (!RegExp(AppConstants.phonePattern).hasMatch(value.trim())) {
          return 'Please enter a valid phone number';
        }
        return null;
      },
      onChanged: onChanged,
      onFieldSubmitted: onSubmitted,
      enabled: enabled,
      readOnly: readOnly,
      autofocus: autofocus,
      focusNode: focusNode,
    );
  }
}

class SearchTextField extends StatelessWidget {
  final TextEditingController? controller;
  final String? hintText;
  final void Function(String)? onChanged;
  final void Function(String)? onSubmitted;
  final VoidCallback? onClear;
  final bool enabled;
  final bool readOnly;
  final bool autofocus;
  final FocusNode? focusNode;

  const SearchTextField({
    super.key,
    this.controller,
    this.hintText,
    this.onChanged,
    this.onSubmitted,
    this.onClear,
    this.enabled = true,
    this.readOnly = false,
    this.autofocus = false,
    this.focusNode,
  });

  @override
  Widget build(BuildContext context) {
    return CustomTextField(
      controller: controller,
      hintText: hintText ?? 'Search...',
      prefixIcon: const Icon(Icons.search),
      suffixIcon: controller?.text.isNotEmpty == true
          ? IconButton(
              icon: const Icon(Icons.clear),
              onPressed: () {
                controller?.clear();
                onClear?.call();
              },
            )
          : null,
      keyboardType: TextInputType.text,
      textInputAction: TextInputAction.search,
      onChanged: onChanged,
      onFieldSubmitted: onSubmitted,
      enabled: enabled,
      readOnly: readOnly,
      autofocus: autofocus,
      focusNode: focusNode,
      showLabel: false,
      borderRadius: 25,
      contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
    );
  }
}

