a = [
['SIN', 'CJB', 20, 'SGD', '33.00'],
['SIN', 'CJB', 25, 'SGD', '42.00'],
['SIN', 'CJB', 30, 'SGD', '53.00'],
['SIN', 'CJB', 35, 'SGD', '64.00'],
['SIN', 'CJB', 40, 'SGD', '74.00'],
['CJB', 'SIN', 20, 'INR', '1785.00'],
['CJB', 'SIN', 25, 'INR', '2310.00'],
['CJB', 'SIN', 30, 'INR', '2940.00'],
['CJB', 'SIN', 35, 'INR', '3465.00'],
['CJB', 'SIN', 40, 'INR', '3990.00'],
['ICN', 'TPE', 20, 'KRW', '21500.00'],
['ICN', 'TPE', 25, 'KRW', '28100.00'],
['ICN', 'TPE', 30, 'KRW', '36300.00'],
['ICN', 'TPE', 35, 'KRW', '44600.00'],
['ICN', 'TPE', 40, 'KRW', '52800.00'],
['TPE', 'ICN', 20, 'TWD', '600.00'],
['TPE', 'ICN', 25, 'TWD', '780.00'],
['TPE', 'ICN', 30, 'TWD', '1010.00'],
['TPE', 'ICN', 35, 'TWD', '1240.00'],
['TPE', 'ICN', 40, 'TWD', '1470.00'],
['TPE', 'NRT', 20, 'TWD', '760.00'],
['TPE', 'NRT', 25, 'TWD', '875.00'],
['TPE', 'NRT', 30, 'TWD', '1105.00'],
['TPE', 'NRT', 35, 'TWD', '1335.00'],
['TPE', 'NRT', 40, 'TWD', '1565.00'],
['KMG', 'SIN', 20, 'CNY', '160.00'],
['KMG', 'SIN', 25, 'CNY', '190.00'],
['KMG', 'SIN', 30, 'CNY', '245.00'],
['KMG', 'SIN', 35, 'CNY', '295.00'],
['KMG', 'SIN', 40, 'CNY', '345.00'],
['CSX', 'SIN', 20, 'CNY', '185.00'],
['CSX', 'SIN', 25, 'CNY', '220.00'],
['CSX', 'SIN', 30, 'CNY', '270.00'],
['CSX', 'SIN', 35, 'CNY', '320.00'],
['CSX', 'SIN', 40, 'CNY', '370.00'],
['TXL', 'SIN', 20, 'EUR', '44.00'],
['TXL', 'SIN', 25, 'EUR', '53.00'],
['TXL', 'SIN', 30, 'EUR', '66.00'],
['TXL', 'SIN', 35, 'EUR', '79.00'],
['TXL', 'SIN', 40, 'EUR', '92.00'],
['CRK', 'SIN', 20, 'PHP', '1320.00'],
['CRK', 'SIN', 25, 'PHP', '1640.00'],
['CRK', 'SIN', 30, 'PHP', '2040.00'],
['CRK', 'SIN', 35, 'PHP', '2440.00'],
['CRK', 'SIN', 40, 'PHP', '2840.00'],
['MNL', 'SIN', 20, 'PHP', '1320.00'],
['MNL', 'SIN', 25, 'PHP', '1640.00'],
['MNL', 'SIN', 30, 'PHP', '2040.00'],
['MNL', 'SIN', 35, 'PHP', '2440.00'],
['MNL', 'SIN', 40, 'PHP', '2840.00'],
['MEL', 'SIN', 20, 'AUD', '47.00'],
['MEL', 'SIN', 25, 'AUD', '56.00'],
['MEL', 'SIN', 30, 'AUD', '69.00'],
['MEL', 'SIN', 35, 'AUD', '81.00'],
['MEL', 'SIN', 40, 'AUD', '93.00'],
['PER', 'SIN', 20, 'AUD', '45.00'],
['PER', 'SIN', 25, 'AUD', '54.00'],
['PER', 'SIN', 30, 'AUD', '66.00'],
['PER', 'SIN', 35, 'AUD', '79.00'],
['PER', 'SIN', 40, 'AUD', '91.00'],
['SYD', 'SIN', 20, 'AUD', '50.00'],
['SYD', 'SIN', 25, 'AUD', '57.00'],
['SYD', 'SIN', 30, 'AUD', '70.00'],
['SYD', 'SIN', 35, 'AUD', '81.00'],
['SYD', 'SIN', 40, 'AUD', '91.00'],
['ICN', 'SIN', 20, 'KRW', '37100.00'],
['ICN', 'SIN', 25, 'KRW', '43700.00'],
['ICN', 'SIN', 30, 'KRW', '52800.00'],
['ICN', 'SIN', 35, 'KRW', '64400.00'],
['ICN', 'SIN', 40, 'KRW', '74300.00'],
['HKG', 'SIN', 20, 'HKD', '185.00'],
['HKG', 'SIN', 25, 'HKD', '240.00'],
['HKG', 'SIN', 30, 'HKD', '290.00'],
['HKG', 'SIN', 35, 'HKD', '360.00'],
['HKG', 'SIN', 40, 'HKD', '420.00'],
['MAA', 'SIN', 20, 'INR', '1995.00'],
['MAA', 'SIN', 25, 'INR', '2310.00'],
['MAA', 'SIN', 30, 'INR', '2940.00'],
['MAA', 'SIN', 35, 'INR', '3360.00'],
['MAA', 'SIN', 40, 'INR', '3885.00'],
['ATQ', 'SIN', 20, 'INR', '2415.00'],
['ATQ', 'SIN', 25, 'INR', '2940.00'],
['ATQ', 'SIN', 30, 'INR', '3570.00'],
['ATQ', 'SIN', 35, 'INR', '4095.00'],
['ATQ', 'SIN', 40, 'INR', '4935.00'],
['TRV', 'SIN', 20, 'INR', '1890.00'],
['TRV', 'SIN', 25, 'INR', '2310.00'],
['TRV', 'SIN', 30, 'INR', '2940.00'],
['TRV', 'SIN', 35, 'INR', '3465.00'],
['TRV', 'SIN', 40, 'INR', '3990.00'],
['TRZ', 'SIN', 20, 'INR', '1995.00'],
['TRZ', 'SIN', 25, 'INR', '2310.00'],
['TRZ', 'SIN', 30, 'INR', '2940.00'],
['TRZ', 'SIN', 35, 'INR', '3360.00'],
['TRZ', 'SIN', 40, 'INR', '3990.00'],
['HAN', 'SIN', 20, 'VND', '518000.00'],
['HAN', 'SIN', 25, 'VND', '673000.00'],
['HAN', 'SIN', 30, 'VND', '828000.00'],
['HAN', 'SIN', 35, 'VND', '1001000.00'],
['HAN', 'SIN', 40, 'VND', '1173000.00'],
['KCH', 'SIN', 20, 'MYR', '70.00'],
['KCH', 'SIN', 25, 'MYR', '100.00'],
['KCH', 'SIN', 30, 'MYR', '135.00'],
['KCH', 'SIN', 35, 'MYR', '165.00'],
['KCH', 'SIN', 40, 'MYR', '195.00'],
['KUL', 'SIN', 20, 'MYR', '70.00'],
['KUL', 'SIN', 25, 'MYR', '100.00'],
['KUL', 'SIN', 30, 'MYR', '135.00'],
['KUL', 'SIN', 35, 'MYR', '165.00'],
['KUL', 'SIN', 40, 'MYR', '195.00'],
['LGK', 'SIN', 20, 'MYR', '75.00'],
['LGK', 'SIN', 25, 'MYR', '100.00'],
['LGK', 'SIN', 30, 'MYR', '135.00'],
['LGK', 'SIN', 35, 'MYR', '165.00'],
['LGK', 'SIN', 40, 'MYR', '195.00'],
['KBR', 'SIN', 20, 'MYR', '70.00'],
['KBR', 'SIN', 25, 'MYR', '100.00'],
['KBR', 'SIN', 30, 'MYR', '130.00'],
['KBR', 'SIN', 35, 'MYR', '160.00'],
['KBR', 'SIN', 40, 'MYR', '190.00'],
['KUA', 'SIN', 20, 'MYR', '75.00'],
['KUA', 'SIN', 25, 'MYR', '100.00'],
['KUA', 'SIN', 30, 'MYR', '135.00'],
['KUA', 'SIN', 35, 'MYR', '165.00'],
['KUA', 'SIN', 40, 'MYR', '195.00'],
['PEN', 'SIN', 20, 'MYR', '70.00'],
['PEN', 'SIN', 25, 'MYR', '100.00'],
['PEN', 'SIN', 30, 'MYR', '135.00'],
['PEN', 'SIN', 35, 'MYR', '165.00'],
['PEN', 'SIN', 40, 'MYR', '195.00'],
['TNA', 'SIN', 20, 'CNY', '215.00'],
['TNA', 'SIN', 25, 'CNY', '260.00'],
['TNA', 'SIN', 30, 'CNY', '320.00'],
['TNA', 'SIN', 35, 'CNY', '390.00'],
['TNA', 'SIN', 40, 'CNY', '450.00'],
['KHN', 'SIN', 20, 'CNY', '175.00'],
['KHN', 'SIN', 25, 'CNY', '210.00'],
['KHN', 'SIN', 30, 'CNY', '260.00'],
['KHN', 'SIN', 35, 'CNY', '320.00'],
['KHN', 'SIN', 40, 'CNY', '370.00'],
['FOC', 'SIN', 20, 'CNY', '185.00'],
['FOC', 'SIN', 25, 'CNY', '220.00'],
['FOC', 'SIN', 30, 'CNY', '270.00'],
['FOC', 'SIN', 35, 'CNY', '320.00'],
['FOC', 'SIN', 40, 'CNY', '370.00'],
['BKI', 'SIN', 20, 'MYR', '75.00'],
['BKI', 'SIN', 25, 'MYR', '100.00'],
['BKI', 'SIN', 30, 'MYR', '130.00'],
['BKI', 'SIN', 35, 'MYR', '165.00'],
['BKI', 'SIN', 40, 'MYR', '195.00'],
['SIN', 'KHN', 20, 'SGD', '35.00'],
['SIN', 'KHN', 25, 'SGD', '42.00'],
['SIN', 'KHN', 30, 'SGD', '52.00'],
['SIN', 'KHN', 35, 'SGD', '64.00'],
['SIN', 'KHN', 40, 'SGD', '74.00'],
['SIN', 'ICN', 20, 'SGD', '45.00'],
['SIN', 'ICN', 25, 'SGD', '53.00'],
['SIN', 'ICN', 30, 'SGD', '64.00'],
['SIN', 'ICN', 35, 'SGD', '78.00'],
['SIN', 'ICN', 40, 'SGD', '90.00'],
['IPH', 'SIN', 20, 'MYR', '70.00'],
['IPH', 'SIN', 25, 'MYR', '100.00'],
['IPH', 'SIN', 30, 'MYR', '135.00'],
['IPH', 'SIN', 35, 'MYR', '165.00'],
['IPH', 'SIN', 40, 'MYR', '195.00'],
['CNX', 'SIN', 20, 'THB', '770.00'],
['CNX', 'SIN', 25, 'THB', '940.00'],
['CNX', 'SIN', 30, 'THB', '1200.00'],
['CNX', 'SIN', 35, 'THB', '1440.00'],
['CNX', 'SIN', 40, 'THB', '1680.00'],
['KBV', 'SIN', 20, 'THB', '650.00'],
['KBV', 'SIN', 25, 'THB', '820.00'],
['KBV', 'SIN', 30, 'THB', '1105.00'],
['KBV', 'SIN', 35, 'THB', '1345.00'],
['KBV', 'SIN', 40, 'THB', '1585.00'],
['DMK', 'SIN', 20, 'THB', '650.00'],
['DMK', 'SIN', 25, 'THB', '820.00'],
['DMK', 'SIN', 30, 'THB', '1060.00'],
['DMK', 'SIN', 35, 'THB', '1345.00'],
['DMK', 'SIN', 40, 'THB', '1585.00'],
['BKK', 'SIN', 20, 'THB', '675.00'],
['BKK', 'SIN', 25, 'THB', '840.00'],
['BKK', 'SIN', 30, 'THB', '1060.00'],
['BKK', 'SIN', 35, 'THB', '1345.00'],
['BKK', 'SIN', 40, 'THB', '1585.00'],
['HDY', 'SIN', 20, 'THB', '625.00'],
['HDY', 'SIN', 25, 'THB', '820.00'],
['HDY', 'SIN', 30, 'THB', '1105.00'],
['HDY', 'SIN', 35, 'THB', '1345.00'],
['HDY', 'SIN', 40, 'THB', '1585.00'],
['HKT', 'SIN', 20, 'THB', '650.00'],
['HKT', 'SIN', 25, 'THB', '820.00'],
['HKT', 'SIN', 30, 'THB', '1105.00'],
['HKT', 'SIN', 35, 'THB', '1345.00'],
['HKT', 'SIN', 40, 'THB', '1585.00'],
['KIX', 'SIN', 20, 'JPY', '3700.00'],
['KIX', 'SIN', 25, 'JPY', '4400.00'],
['KIX', 'SIN', 30, 'JPY', '5400.00'],
['KIX', 'SIN', 35, 'JPY', '6400.00'],
['KIX', 'SIN', 40, 'JPY', '7400.00'],
['KHH', 'SIN', 20, 'TWD', '760.00'],
['KHH', 'SIN', 25, 'TWD', '945.00'],
['KHH', 'SIN', 30, 'TWD', '1175.00'],
['KHH', 'SIN', 35, 'TWD', '1425.00'],
['KHH', 'SIN', 40, 'TWD', '1655.00'],
['SHE', 'SIN', 20, 'CNY', '225.00'],
['SHE', 'SIN', 25, 'CNY', '270.00'],
['SHE', 'SIN', 30, 'CNY', '330.00'],
['SHE', 'SIN', 35, 'CNY', '390.00'],
['SHE', 'SIN', 40, 'CNY', '450.00'],
['HGH', 'SIN', 20, 'CNY', '175.00'],
['HGH', 'SIN', 25, 'CNY', '210.00'],
['HGH', 'SIN', 30, 'CNY', '265.00'],
['HGH', 'SIN', 35, 'CNY', '320.00'],
['HGH', 'SIN', 40, 'CNY', '370.00'],
['NKG', 'SIN', 20, 'CNY', '225.00'],
['NKG', 'SIN', 25, 'CNY', '260.00'],
['NKG', 'SIN', 30, 'CNY', '320.00'],
['NKG', 'SIN', 35, 'CNY', '390.00'],
['NKG', 'SIN', 40, 'CNY', '450.00'],
['CAN', 'SIN', 20, 'CNY', '165.00'],
['CAN', 'SIN', 25, 'CNY', '195.00'],
['CAN', 'SIN', 30, 'CNY', '250.00'],
['CAN', 'SIN', 35, 'CNY', '300.00'],
['CAN', 'SIN', 40, 'CNY', '350.00'],
['CGO', 'SIN', 20, 'CNY', '210.00'],
['CGO', 'SIN', 25, 'CNY', '270.00'],
['CGO', 'SIN', 30, 'CNY', '315.00'],
['CGO', 'SIN', 35, 'CNY', '370.00'],
['CGO', 'SIN', 40, 'CNY', '440.00'],
['WUH', 'SIN', 20, 'CNY', '185.00'],
['WUH', 'SIN', 25, 'CNY', '220.00'],
['WUH', 'SIN', 30, 'CNY', '270.00'],
['WUH', 'SIN', 35, 'CNY', '320.00'],
['WUH', 'SIN', 40, 'CNY', '370.00'],
['HRB', 'SIN', 20, 'CNY', '230.00'],
['HRB', 'SIN', 25, 'CNY', '265.00'],
['HRB', 'SIN', 30, 'CNY', '325.00'],
['HRB', 'SIN', 35, 'CNY', '380.00'],
['HRB', 'SIN', 40, 'CNY', '450.00'],
['PKU', 'SIN', 20, 'IDR', '263000.00'],
['PKU', 'SIN', 25, 'IDR', '347000.00'],
['PKU', 'SIN', 30, 'IDR', '462000.00'],
['PKU', 'SIN', 35, 'IDR', '567000.00'],
['PKU', 'SIN', 40, 'IDR', '672000.00'],
['CGK', 'SIN', 20, 'IDR', '273000.00'],
['CGK', 'SIN', 25, 'IDR', '357000.00'],
['CGK', 'SIN', 30, 'IDR', '483000.00'],
['CGK', 'SIN', 35, 'IDR', '588000.00'],
['CGK', 'SIN', 40, 'IDR', '693000.00'],
['SUB', 'SIN', 20, 'IDR', '263000.00'],
['SUB', 'SIN', 25, 'IDR', '336000.00'],
['SUB', 'SIN', 30, 'IDR', '483000.00'],
['SUB', 'SIN', 35, 'IDR', '588000.00'],
['SUB', 'SIN', 40, 'IDR', '693000.00'],
['PLM', 'SIN', 20, 'IDR', '263000.00'],
['PLM', 'SIN', 25, 'IDR', '347000.00'],
['PLM', 'SIN', 30, 'IDR', '462000.00'],
['PLM', 'SIN', 35, 'IDR', '567000.00'],
['PLM', 'SIN', 40, 'IDR', '672000.00'],
['DPS', 'SIN', 20, 'IDR', '294000.00'],
['DPS', 'SIN', 25, 'IDR', '378000.00'],
['DPS', 'SIN', 30, 'IDR', '483000.00'],
['DPS', 'SIN', 35, 'IDR', '588000.00'],
['DPS', 'SIN', 40, 'IDR', '693000.00'],
['SIN', 'HAN', 20, 'SGD', '30.00'],
['SIN', 'HAN', 25, 'SGD', '39.00'],
['SIN', 'HAN', 30, 'SGD', '48.00'],
['SIN', 'HAN', 35, 'SGD', '58.00'],
['SIN', 'HAN', 40, 'SGD', '68.00'],
['SIN', 'HKT', 20, 'SGD', '27.00'],
['SIN', 'HKT', 25, 'SGD', '34.00'],
['SIN', 'HKT', 30, 'SGD', '46.00'],
['SIN', 'HKT', 35, 'SGD', '56.00'],
['SIN', 'HKT', 40, 'SGD', '66.00'],
['SIN', 'HDY', 20, 'SGD', '26.00'],
['SIN', 'HDY', 25, 'SGD', '34.00'],
['SIN', 'HDY', 30, 'SGD', '46.00'],
['SIN', 'HDY', 35, 'SGD', '56.00'],
['SIN', 'HDY', 40, 'SGD', '66.00'],
['SIN', 'CNX', 20, 'SGD', '32.00'],
['SIN', 'CNX', 25, 'SGD', '39.00'],
['SIN', 'CNX', 30, 'SGD', '50.00'],
['SIN', 'CNX', 35, 'SGD', '60.00'],
['SIN', 'CNX', 40, 'SGD', '70.00'],
['SIN', 'DMK', 20, 'SGD', '27.00'],
['SIN', 'DMK', 25, 'SGD', '34.00'],
['SIN', 'DMK', 30, 'SGD', '44.00'],
['SIN', 'DMK', 35, 'SGD', '56.00'],
['SIN', 'DMK', 40, 'SGD', '66.00'],
['SIN', 'KHH', 20, 'SGD', '33.00'],
['SIN', 'KHH', 25, 'SGD', '41.00'],
['SIN', 'KHH', 30, 'SGD', '51.00'],
['SIN', 'KHH', 35, 'SGD', '62.00'],
['SIN', 'KHH', 40, 'SGD', '72.00'],
['SIN', 'MNL', 20, 'SGD', '32.00'],
['SIN', 'MNL', 25, 'SGD', '41.00'],
['SIN', 'MNL', 30, 'SGD', '51.00'],
['SIN', 'MNL', 35, 'SGD', '61.00'],
['SIN', 'MNL', 40, 'SGD', '71.00'],
['SIN', 'CEB', 20, 'SGD', '31.00'],
['SIN', 'CEB', 25, 'SGD', '41.00'],
['SIN', 'CEB', 30, 'SGD', '51.00'],
['SIN', 'CEB', 35, 'SGD', '61.00'],
['SIN', 'CEB', 40, 'SGD', '71.00'],
['SIN', 'PEN', 20, 'SGD', '24.00'],
['SIN', 'PEN', 25, 'SGD', '34.00'],
['SIN', 'PEN', 30, 'SGD', '46.00'],
['SIN', 'PEN', 35, 'SGD', '56.00'],
['SIN', 'PEN', 40, 'SGD', '66.00'],
['SIN', 'LGK', 20, 'SGD', '25.00'],
['SIN', 'LGK', 25, 'SGD', '34.00'],
['SIN', 'LGK', 30, 'SGD', '46.00'],
['SIN', 'LGK', 35, 'SGD', '56.00'],
['SIN', 'LGK', 40, 'SGD', '66.00'],
['SIN', 'KCH', 20, 'SGD', '24.00'],
['SIN', 'KCH', 25, 'SGD', '34.00'],
['SIN', 'KCH', 30, 'SGD', '46.00'],
['SIN', 'KCH', 35, 'SGD', '56.00'],
['SIN', 'KCH', 40, 'SGD', '66.00'],
['SIN', 'KUA', 20, 'SGD', '26.00'],
['SIN', 'KUA', 25, 'SGD', '34.00'],
['SIN', 'KUA', 30, 'SGD', '46.00'],
['SIN', 'KUA', 35, 'SGD', '56.00'],
['SIN', 'KUA', 40, 'SGD', '66.00'],
['SIN', 'KBR', 20, 'SGD', '24.00'],
['SIN', 'KBR', 25, 'SGD', '33.00'],
['SIN', 'KBR', 30, 'SGD', '44.00'],
['SIN', 'KBR', 35, 'SGD', '54.00'],
['SIN', 'KBR', 40, 'SGD', '64.00'],
['SIN', 'MFM', 20, 'SGD', '33.00'],
['SIN', 'MFM', 25, 'SGD', '40.00'],
['SIN', 'MFM', 30, 'SGD', '50.00'],
['SIN', 'MFM', 35, 'SGD', '60.00'],
['SIN', 'MFM', 40, 'SGD', '70.00'],
['SIN', 'NRT', 20, 'SGD', '43.00'],
['SIN', 'NRT', 25, 'SGD', '52.00'],
['SIN', 'NRT', 30, 'SGD', '64.00'],
['SIN', 'NRT', 35, 'SGD', '78.00'],
['SIN', 'NRT', 40, 'SGD', '90.00'],
['SIN', 'KIX', 20, 'SGD', '45.00'],
['SIN', 'KIX', 25, 'SGD', '53.00'],
['SIN', 'KIX', 30, 'SGD', '66.00'],
['SIN', 'KIX', 35, 'SGD', '78.00'],
['SIN', 'KIX', 40, 'SGD', '90.00'],
['SIN', 'SUB', 20, 'SGD', '25.00'],
['SIN', 'SUB', 25, 'SGD', '32.00'],
['SIN', 'SUB', 30, 'SGD', '46.00'],
['SIN', 'SUB', 35, 'SGD', '56.00'],
['SIN', 'SUB', 40, 'SGD', '66.00'],
['SIN', 'PLM', 20, 'SGD', '25.00'],
['SIN', 'PLM', 25, 'SGD', '33.00'],
['SIN', 'PLM', 30, 'SGD', '44.00'],
['SIN', 'PLM', 35, 'SGD', '54.00'],
['SIN', 'PLM', 40, 'SGD', '64.00'],
['SIN', 'CGK', 20, 'SGD', '26.00'],
['SIN', 'CGK', 25, 'SGD', '34.00'],
['SIN', 'CGK', 30, 'SGD', '46.00'],
['SIN', 'CGK', 35, 'SGD', '56.00'],
['SIN', 'CGK', 40, 'SGD', '66.00'],
['SIN', 'DPS', 20, 'SGD', '28.00'],
['SIN', 'DPS', 25, 'SGD', '36.00'],
['SIN', 'DPS', 30, 'SGD', '46.00'],
['SIN', 'DPS', 35, 'SGD', '56.00'],
['SIN', 'DPS', 40, 'SGD', '66.00'],
['SIN', 'TRV', 20, 'SGD', '35.00'],
['SIN', 'TRV', 25, 'SGD', '42.00'],
['SIN', 'TRV', 30, 'SGD', '53.00'],
['SIN', 'TRV', 35, 'SGD', '64.00'],
['SIN', 'TRV', 40, 'SGD', '74.00'],
['SIN', 'TRZ', 20, 'SGD', '37.00'],
['SIN', 'TRZ', 25, 'SGD', '42.00'],
['SIN', 'TRZ', 30, 'SGD', '55.00'],
['SIN', 'TRZ', 35, 'SGD', '62.00'],
['SIN', 'TRZ', 40, 'SGD', '74.00'],
['SIN', 'HYD', 20, 'SGD', '37.00'],
['SIN', 'HYD', 25, 'SGD', '44.00'],
['SIN', 'HYD', 30, 'SGD', '54.00'],
['SIN', 'HYD', 35, 'SGD', '64.00'],
['SIN', 'HYD', 40, 'SGD', '74.00'],
['SIN', 'MAA', 20, 'SGD', '38.00'],
['SIN', 'MAA', 25, 'SGD', '43.00'],
['SIN', 'MAA', 30, 'SGD', '55.00'],
['SIN', 'MAA', 35, 'SGD', '62.00'],
['SIN', 'MAA', 40, 'SGD', '72.00'],
['SIN', 'ATQ', 20, 'SGD', '45.00'],
['SIN', 'ATQ', 25, 'SGD', '52.00'],
['SIN', 'ATQ', 30, 'SGD', '65.00'],
['SIN', 'ATQ', 35, 'SGD', '76.00'],
['SIN', 'ATQ', 40, 'SGD', '90.00'],
['SIN', 'HKG', 20, 'SGD', '31.00'],
['SIN', 'HKG', 25, 'SGD', '40.00'],
['SIN', 'HKG', 30, 'SGD', '50.00'],
['SIN', 'HKG', 35, 'SGD', '60.00'],
['SIN', 'HKG', 40, 'SGD', '70.00'],
['SIN', 'XIY', 20, 'SGD', '43.00'],
['SIN', 'XIY', 25, 'SGD', '56.00'],
['SIN', 'XIY', 30, 'SGD', '65.00'],
['SIN', 'XIY', 35, 'SGD', '78.00'],
['SIN', 'XIY', 40, 'SGD', '90.00'],
['SIN', 'WUH', 20, 'SGD', '37.00'],
['SIN', 'WUH', 25, 'SGD', '44.00'],
['SIN', 'WUH', 30, 'SGD', '54.00'],
['SIN', 'WUH', 35, 'SGD', '64.00'],
['SIN', 'WUH', 40, 'SGD', '74.00'],
['SIN', 'TSN', 20, 'SGD', '43.00'],
['SIN', 'TSN', 25, 'SGD', '52.00'],
['SIN', 'TSN', 30, 'SGD', '64.00'],
['SIN', 'TSN', 35, 'SGD', '78.00'],
['SIN', 'TSN', 40, 'SGD', '90.00'],
['SIN', 'SHE', 20, 'SGD', '45.00'],
['SIN', 'SHE', 25, 'SGD', '53.00'],
['SIN', 'SHE', 30, 'SGD', '65.00'],
['SIN', 'SHE', 35, 'SGD', '78.00'],
['SIN', 'SHE', 40, 'SGD', '90.00'],
['SIN', 'TAO', 20, 'SGD', '46.00'],
['SIN', 'TAO', 25, 'SGD', '53.00'],
['SIN', 'TAO', 30, 'SGD', '65.00'],
['SIN', 'TAO', 35, 'SGD', '78.00'],
['SIN', 'TAO', 40, 'SGD', '90.00'],
['SIN', 'NKG', 20, 'SGD', '46.00'],
['SIN', 'NKG', 25, 'SGD', '53.00'],
['SIN', 'NKG', 30, 'SGD', '64.00'],
['SIN', 'NKG', 35, 'SGD', '78.00'],
['SIN', 'NKG', 40, 'SGD', '90.00'],
['SIN', 'KMG', 20, 'SGD', '32.00'],
['SIN', 'KMG', 25, 'SGD', '38.00'],
['SIN', 'KMG', 30, 'SGD', '49.00'],
['SIN', 'KMG', 35, 'SGD', '59.00'],
['SIN', 'KMG', 40, 'SGD', '69.00'],
['SIN', 'HGH', 20, 'SGD', '35.00'],
['SIN', 'HGH', 25, 'SGD', '42.00'],
['SIN', 'HGH', 30, 'SGD', '53.00'],
['SIN', 'HGH', 35, 'SGD', '64.00'],
['SIN', 'HGH', 40, 'SGD', '74.00'],
['SIN', 'CAN', 20, 'SGD', '33.00'],
['SIN', 'CAN', 25, 'SGD', '40.00'],
['SIN', 'CAN', 30, 'SGD', '50.00'],
['SIN', 'CAN', 35, 'SGD', '60.00'],
['SIN', 'CAN', 40, 'SGD', '70.00'],
['SIN', 'CSX', 20, 'SGD', '37.00'],
['SIN', 'CSX', 25, 'SGD', '44.00'],
['SIN', 'CSX', 30, 'SGD', '54.00'],
['SIN', 'CSX', 35, 'SGD', '64.00'],
['SIN', 'CSX', 40, 'SGD', '74.00'],
['SIN', 'SYD', 20, 'SGD', '50.00'],
['SIN', 'SYD', 25, 'SGD', '57.00'],
['SIN', 'SYD', 30, 'SGD', '69.00'],
['SIN', 'SYD', 35, 'SGD', '81.00'],
['SIN', 'SYD', 40, 'SGD', '91.00'],
['SIN', 'PER', 20, 'SGD', '44.00'],
['SIN', 'PER', 25, 'SGD', '55.00'],
['SIN', 'PER', 30, 'SGD', '67.00'],
['SIN', 'PER', 35, 'SGD', '79.00'],
['SIN', 'PER', 40, 'SGD', '91.00'],
['SIN', 'MEL', 20, 'SGD', '47.00'],
['SIN', 'MEL', 25, 'SGD', '56.00'],
['SIN', 'MEL', 30, 'SGD', '69.00'],
['SIN', 'MEL', 35, 'SGD', '81.00'],
['SIN', 'MEL', 40, 'SGD', '93.00'],
['SIN', 'OOL', 20, 'SGD', '47.00'],
['SIN', 'OOL', 25, 'SGD', '55.00'],
['SIN', 'OOL', 30, 'SGD', '67.00'],
['SIN', 'OOL', 35, 'SGD', '78.00'],
['SIN', 'OOL', 40, 'SGD', '90.00'],
['VTZ', 'SIN', 20, 'INR', '1785.00'],
['VTZ', 'SIN', 25, 'INR', '2310.00'],
['VTZ', 'SIN', 30, 'INR', '2940.00'],
['VTZ', 'SIN', 35, 'INR', '3465.00'],
['VTZ', 'SIN', 40, 'INR', '3990.00'],
['NRT', 'TPE', 20, 'JPY', '2700.00'],
['NRT', 'TPE', 25, 'JPY', '3100.00'],
['NRT', 'TPE', 30, 'JPY', '4000.00'],
['NRT', 'TPE', 35, 'JPY', '4800.00'],
['NRT', 'TPE', 40, 'JPY', '5600.00'],
['MFM', 'SIN', 20, 'HKD', '195.00'],
['MFM', 'SIN', 25, 'HKD', '240.00'],
['MFM', 'SIN', 30, 'HKD', '300.00'],
['MFM', 'SIN', 35, 'HKD', '360.00'],
['MFM', 'SIN', 40, 'HKD', '420.00'],
['SGN', 'SIN', 20, 'VND', '466000.00'],
['SGN', 'SIN', 25, 'VND', '587000.00'],
['SGN', 'SIN', 30, 'VND', '760000.00'],
['SGN', 'SIN', 35, 'VND', '967000.00'],
['SGN', 'SIN', 40, 'VND', '1139000.00'],
['SIN', 'TNA', 20, 'SGD', '43.00'],
['SIN', 'TNA', 25, 'SGD', '52.00'],
['SIN', 'TNA', 30, 'SGD', '64.00'],
['SIN', 'TNA', 35, 'SGD', '78.00'],
['SIN', 'TNA', 40, 'SGD', '90.00'],
['SIN', 'FOC', 20, 'SGD', '37.00'],
['SIN', 'FOC', 25, 'SGD', '44.00'],
['SIN', 'FOC', 30, 'SGD', '54.00'],
['SIN', 'FOC', 35, 'SGD', '64.00'],
['SIN', 'FOC', 40, 'SGD', '74.00'],
['SIN', 'BKI', 20, 'SGD', '26.00'],
['SIN', 'BKI', 25, 'SGD', '34.00'],
['SIN', 'BKI', 30, 'SGD', '44.00'],
['SIN', 'BKI', 35, 'SGD', '56.00'],
['SIN', 'BKI', 40, 'SGD', '66.00'],
['NRT', 'SIN', 20, 'JPY', '3500.00'],
['NRT', 'SIN', 25, 'JPY', '4300.00'],
['NRT', 'SIN', 30, 'JPY', '5300.00'],
['NRT', 'SIN', 35, 'JPY', '6400.00'],
['NRT', 'SIN', 40, 'JPY', '7400.00'],
['TPE', 'SIN', 20, 'TWD', '780.00'],
['TPE', 'SIN', 25, 'TWD', '945.00'],
['TPE', 'SIN', 30, 'TWD', '1175.00'],
['TPE', 'SIN', 35, 'TWD', '1425.00'],
['TPE', 'SIN', 40, 'TWD', '1655.00'],
['TSN', 'SIN', 20, 'CNY', '215.00'],
['TSN', 'SIN', 25, 'CNY', '260.00'],
['TSN', 'SIN', 30, 'CNY', '320.00'],
['TSN', 'SIN', 35, 'CNY', '390.00'],
['TSN', 'SIN', 40, 'CNY', '450.00'],
['TAO', 'SIN', 20, 'CNY', '235.00'],
['TAO', 'SIN', 25, 'CNY', '265.00'],
['TAO', 'SIN', 30, 'CNY', '325.00'],
['TAO', 'SIN', 35, 'CNY', '390.00'],
['TAO', 'SIN', 40, 'CNY', '450.00'],
['SIN', 'SGN', 20, 'SGD', '27.00'],
['SIN', 'SGN', 25, 'SGD', '34.00'],
['SIN', 'SGN', 30, 'SGD', '44.00'],
['SIN', 'SGN', 35, 'SGD', '56.00'],
['SIN', 'SGN', 40, 'SGD', '66.00'],
['SIN', 'KBV', 20, 'SGD', '27.00'],
['SIN', 'KBV', 25, 'SGD', '34.00'],
['SIN', 'KBV', 30, 'SGD', '46.00'],
['SIN', 'KBV', 35, 'SGD', '56.00'],
['SIN', 'KBV', 40, 'SGD', '66.00'],
['SIN', 'BKK', 20, 'SGD', '27.00'],
['SIN', 'BKK', 25, 'SGD', '34.00'],
['SIN', 'BKK', 30, 'SGD', '44.00'],
['SIN', 'BKK', 35, 'SGD', '56.00'],
['SIN', 'BKK', 40, 'SGD', '66.00'],
['SIN', 'TPE', 20, 'SGD', '34.00'],
['SIN', 'TPE', 25, 'SGD', '41.00'],
['SIN', 'TPE', 30, 'SGD', '51.00'],
['SIN', 'TPE', 35, 'SGD', '62.00'],
['SIN', 'TPE', 40, 'SGD', '72.00'],
['SIN', 'KUL', 20, 'SGD', '24.00'],
['SIN', 'KUL', 25, 'SGD', '34.00'],
['SIN', 'KUL', 30, 'SGD', '46.00'],
['SIN', 'KUL', 35, 'SGD', '56.00'],
['SIN', 'KUL', 40, 'SGD', '66.00'],
['SIN', 'IPH', 20, 'SGD', '24.00'],
['SIN', 'IPH', 25, 'SGD', '34.00'],
['SIN', 'IPH', 30, 'SGD', '46.00'],
['SIN', 'IPH', 35, 'SGD', '56.00'],
['SIN', 'IPH', 40, 'SGD', '66.00'],
['SIN', 'TXL', 20, 'SGD', '67.00'],
['SIN', 'TXL', 25, 'SGD', '81.00'],
['SIN', 'TXL', 30, 'SGD', '101.00'],
['SIN', 'TXL', 35, 'SGD', '122.00'],
['SIN', 'TXL', 40, 'SGD', '142.00'],
['SIN', 'CGO', 20, 'SGD', '42.00'],
['SIN', 'CGO', 25, 'SGD', '54.00'],
['SIN', 'CGO', 30, 'SGD', '63.00'],
['SIN', 'CGO', 35, 'SGD', '74.00'],
['SIN', 'CGO', 40, 'SGD', '88.00'],
['SIN', 'HRB', 20, 'SGD', '46.00'],
['SIN', 'HRB', 25, 'SGD', '53.00'],
['SIN', 'HRB', 30, 'SGD', '65.00'],
['SIN', 'HRB', 35, 'SGD', '76.00'],
['SIN', 'HRB', 40, 'SGD', '90.00'],
['SIN', 'VTZ', 20, 'SGD', '33.00'],
['SIN', 'VTZ', 25, 'SGD', '42.00'],
['SIN', 'VTZ', 30, 'SGD', '53.00'],
['SIN', 'VTZ', 35, 'SGD', '64.00'],
['SIN', 'VTZ', 40, 'SGD', '74.00'],
['HYD', 'SIN', 20, 'INR', '1995.00'],
['HYD', 'SIN', 25, 'INR', '2415.00'],
['HYD', 'SIN', 30, 'INR', '2940.00'],
['HYD', 'SIN', 35, 'INR', '3465.00'],
['HYD', 'SIN', 40, 'INR', '3990.00'],
['SIN', 'CRK', 20, 'SGD', '33.00'],
['SIN', 'CRK', 25, 'SGD', '41.00'],
['SIN', 'CRK', 30, 'SGD', '51.00'],
['SIN', 'CRK', 35, 'SGD', '61.00'],
['SIN', 'CRK', 40, 'SGD', '71.00'],
['SIN', 'PKU', 20, 'SGD', '25.00'],
['SIN', 'PKU', 25, 'SGD', '33.00'],
['SIN', 'PKU', 30, 'SGD', '44.00'],
['SIN', 'PKU', 35, 'SGD', '54.00'],
['SIN', 'PKU', 40, 'SGD', '64.00'],
['KIX', 'DMK', 20, 'JPY', '3200.00'],
['KIX', 'DMK', 25, 'JPY', '4200.00'],
['KIX', 'DMK', 30, 'JPY', '5200.00'],
['KIX', 'DMK', 35, 'JPY', '6100.00'],
['KIX', 'DMK', 40, 'JPY', '7100.00'],
['KIX', 'DMK', 50, 'JPY', '10400.00'],
['KIX', 'DMK', 60, 'JPY', '15100.00'],
['KIX', 'DMK', 70, 'JPY', '21500.00'],
['KIX', 'DMK', 80, 'JPY', '28800.00'],
['NRT', 'DMK', 20, 'JPY', '3200.00'],
['NRT', 'DMK', 25, 'JPY', '4200.00'],
['NRT', 'DMK', 30, 'JPY', '5200.00'],
['NRT', 'DMK', 35, 'JPY', '6100.00'],
['NRT', 'DMK', 40, 'JPY', '7100.00'],
['NRT', 'DMK', 50, 'JPY', '10400.00'],
['NRT', 'DMK', 60, 'JPY', '15100.00'],
['NRT', 'DMK', 70, 'JPY', '21500.00'],
['NRT', 'DMK', 80, 'JPY', '28800.00'],
['DMK', 'KIX', 20, 'THB', '1000.00'],
['DMK', 'KIX', 25, 'THB', '1300.00'],
['DMK', 'KIX', 30, 'THB', '1600.00'],
['DMK', 'KIX', 35, 'THB', '1900.00'],
['DMK', 'KIX', 40, 'THB', '2200.00'],
['DMK', 'KIX', 50, 'THB', '3250.00'],
['DMK', 'KIX', 60, 'THB', '4700.00'],
['DMK', 'KIX', 70, 'THB', '6700.00'],
['DMK', 'KIX', 80, 'THB', '9000.00'],
['DMK', 'NRT', 20, 'THB', '1000.00'],
['DMK', 'NRT', 25, 'THB', '1300.00'],
['DMK', 'NRT', 30, 'THB', '1600.00'],
['DMK', 'NRT', 35, 'THB', '1900.00'],
['DMK', 'NRT', 40, 'THB', '2200.00'],
['DMK', 'NRT', 50, 'THB', '3250.00'],
['DMK', 'NRT', 60, 'THB', '4700.00'],
['DMK', 'NRT', 70, 'THB', '6700.00'],
['DMK', 'NRT', 80, 'THB', '9000.00'],
['CTS', 'TPE', 20, 'JPY', '2900.00'],
['CTS', 'TPE', 25, 'JPY', '3500.00'],
['CTS', 'TPE', 30, 'JPY', '4300.00'],
['CTS', 'TPE', 35, 'JPY', '5100.00'],
['CTS', 'TPE', 40, 'JPY', '5900.00'],
['TPE', 'CTS', 20, 'TWD', '805.00'],
['TPE', 'CTS', 25, 'TWD', '965.00'],
['TPE', 'CTS', 30, 'TWD', '1195.00'],
['TPE', 'CTS', 35, 'TWD', '1425.00'],
['TPE', 'CTS', 40, 'TWD', '1655.00'],
['CEB', 'SIN', 20, 'PHP', '1160.00'],
['CEB', 'SIN', 25, 'PHP', '1560.00'],
['CEB', 'SIN', 30, 'PHP', '1920.00'],
['CEB', 'SIN', 35, 'PHP', '2320.00'],
['CEB', 'SIN', 40, 'PHP', '2720.00'],
['WUX', 'SIN', 20, 'CNY', '220.00'],
['WUX', 'SIN', 25, 'CNY', '265.00'],
['WUX', 'SIN', 30, 'CNY', '325.00'],
['WUX', 'SIN', 35, 'CNY', '390.00'],
['WUX', 'SIN', 40, 'CNY', '450.00'],
['XIY', 'SIN', 20, 'CNY', '220.00'],
['XIY', 'SIN', 25, 'CNY', '285.00'],
['XIY', 'SIN', 30, 'CNY', '330.00'],
['XIY', 'SIN', 35, 'CNY', '390.00'],
['XIY', 'SIN', 40, 'CNY', '450.00'],
['SIN', 'WUX', 20, 'SGD', '44.00'],
['SIN', 'WUX', 25, 'SGD', '53.00'],
['SIN', 'WUX', 30, 'SGD', '65.00'],
['SIN', 'WUX', 35, 'SGD', '78.00'],
['SIN', 'WUX', 40, 'SGD', '90.00'],
['ATH', 'SIN', 20, 'EUR', '41.00'],
['ATH', 'SIN', 25, 'EUR', '51.00'],
['ATH', 'SIN', 30, 'EUR', '64.00'],
['ATH', 'SIN', 35, 'EUR', '77.00'],
['ATH', 'SIN', 40, 'EUR', '90.00'],
['SIN', 'ATH', 20, 'SGD', '63.00'],
['SIN', 'ATH', 25, 'SGD', '78.00'],
['SIN', 'ATH', 30, 'SGD', '98.00'],
['SIN', 'ATH', 35, 'SGD', '119.00'],
['SIN', 'ATH', 40, 'SGD', '139.00'],
]

import copy

b = copy.deepcopy(a)
c = copy.deepcopy(a)

for k, v in enumerate(b):
    for i, j in enumerate(c):
        if j[0] == v[0] and j[1] == v[1] and j[2] == v[2]:
            if float(j[4]) > float(v[4]):
                a[k] = j
            else:
                a[i] = v

for n in a:
    print(f"{n},")