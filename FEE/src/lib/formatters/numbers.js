import { config } from '../../config';

function intl_number_format(num) {
  const numValue = num || 0;

  return Intl.NumberFormat(config.supportedLocales, {
    maximumFractionDigits: 3,
  }).format(numValue);
}

export { intl_number_format };
