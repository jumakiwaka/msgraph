import { config } from '../../config';

function intlNumberFormat(num) {
  const numValue = num || 0;

  return Intl.NumberFormat(config.supportedLocales, {
    maximumFractionDigits: 3,
  }).format(numValue);
}

export { intlNumberFormat };
