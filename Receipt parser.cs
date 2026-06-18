using System;
using System.Text.RegularExpressions;

public class ParsedReceipt
{
    public string RawText { get; set; }
    public decimal EstimatedTotal { get; set; }
    public string PaymentMethod { get; set; }

    public ParsedReceipt(string rawText)
    {
        RawText = rawText;
        ParseData();
    }

    private void ParseData()
    {
        // 1. Break the raw text into segments using the pipe delimiter
        string[] segments = RawText.Split('|');

        // Clean up each segment by removing accidental leading/trailing spaces
        for (int i = 0; i < segments.Length; i++)
        {
            segments[i] = segments[i].Trim();
        }

        // 2. Next, we will hunt for our target data points
        ExtractTotal(segments);
        ExtractPaymentMethod(segments);
    }

    private void ExtractTotal(string[] segments)
{
    EstimatedTotal = 0.00m; // Default starting value

    // Loop through each segment we split by the pipe symbol
    for (int i = 0; i < segments.Length; i++)
    {
        // Check if the segment contains common total keywords (case-insensitive)
        if (segments[i].Equals("TOTAL", StringComparison.OrdinalIgnoreCase) || 
            segments[i].Equals("TOTAL SALE", StringComparison.OrdinalIgnoreCase))
        {
            // If we found "TOTAL", the actual amount is usually the next segment!
            if (i + 1 < segments.Length)
            {
                string rawAmount = segments[i + 1];

                // OCR text safety: Replace commas with periods if it used European style (e.g., 19,54 -> 19.54)
                rawAmount = rawAmount.Replace(',', '.');

                // Try to convert the cleaned text string into a proper decimal number
                if (decimal.TryParse(rawAmount, out decimal parsedAmount))
                {
                    EstimatedTotal = parsedAmount;
                    break; // We found it, so we can stop looking!
                }
            }
        }
    }
}
   private void ExtractPaymentMethod(string[] segments)
    {
        PaymentMethod = "Unknown"; // Default starting value

        // Loop through each segment to search for keywords
        for (int i = 0; i < segments.Length; i++)
        {
            string currentSegment = segments[i];

            // Look for common payment terms anywhere inside the segment
            if (currentSegment.Contains("DEBIT", StringComparison.OrdinalIgnoreCase))
            {
                PaymentMethod = "Debit Card";
                break;
            }
            else if (currentSegment.Contains("VISA", StringComparison.OrdinalIgnoreCase))
            {
                PaymentMethod = "Visa";
                break;
            }
            else if (currentSegment.Contains("MASTERCARD", StringComparison.OrdinalIgnoreCase) || 
                     currentSegment.Contains("MC ", StringComparison.OrdinalIgnoreCase))
            {
                PaymentMethod = "Mastercard";
                break;
            }
            else if (currentSegment.Contains("CASH", StringComparison.OrdinalIgnoreCase))
            {
                PaymentMethod = "Cash";
                break;
            }
        }
    }
}