"""
SMC (Smart Money Concept) Strategy for US30 Trading Bot
========================================================

Smart Money Concept strategy that detects:
- Break of Structure (BOS)
- Order Blocks (OB)
- Fair Value Gaps (FVG)
- Market Structure Shift (MSS)
- Liquidity Sweeps

This strategy combines multiple SMC confluences to generate entry signals.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


class SMCStrategy:
    """
    Smart Money Concept strategy for US30.
    
    Detects SMC patterns on M5 timeframe with EMA bias from H1.
    Entry confirmed when:
    1. EMA bias aligned (price above/below EMA on H1)
    2. Break of Structure detected
    3. Market Structure Shift confirmed
    4. At least one of: Order Block, FVG, or Liquidity Sweep present
    """
    
    def __init__(self, config: Dict):
        """
        Initialize SMC strategy.
        
        Args:
            config: Strategy configuration from config_us30.json
        """
        self.config = config
        self.entry_tf = config.get('entry_timeframe', 'M5')
        self.bias_tf = config.get('bias_timeframe', 'H1')
        self.ema_period = config.get('ema_period', 50)
        self.tp_multiplier = config.get('tp_multiplier', 3)
        self.min_candles = config.get('min_candles', 100)
        self.rr_ratio = config.get('rr_ratio', 3)
        
        # Store last detection for logging
        self.last_signal = None
        self.signal_history = []
        
    def analyze(self, entry_data: pd.DataFrame, bias_data: pd.DataFrame) -> Dict:
        """
        Analyze price data for SMC entry signals.
        
        Args:
            entry_data: OHLCV data on entry timeframe (M5)
            bias_data: OHLCV data on bias timeframe (H1)
            
        Returns:
            Dict with signal and details:
            {
                'signal': 'BUY', 'SELL', or 'NONE',
                'strength': 0-100 (confluence score),
                'entry_price': float,
                'stop_loss': float,
                'take_profit': float,
                'details': {'bos': bool, 'ob': bool, 'fvg': bool, ...}
            }
        """
        
        # Validation
        if len(entry_data) < self.min_candles or len(bias_data) < 2:
            return self._no_signal("Insufficient data")
        
        # Step 1: Get EMA bias from H1
        ema_value = self._calculate_ema(bias_data['close'], self.ema_period)
        current_close_h1 = bias_data['close'].iloc[-1]
        
        bullish_bias = current_close_h1 > ema_value
        bearish_bias = current_close_h1 < ema_value
        
        if not (bullish_bias or bearish_bias):
            return self._no_signal("No EMA bias")
        
        # Step 2: Check for SMC entry conditions on M5
        smc_result = self._check_smc_entry(entry_data)
        
        if smc_result['signal'] == 'NONE':
            return self._no_signal("No SMC entry conditions")
        
        # Step 3: Align with bias
        signal = 'NONE'
        if smc_result['type'] == 'BULLISH' and bullish_bias:
            signal = 'BUY'
        elif smc_result['type'] == 'BEARISH' and bearish_bias:
            signal = 'SELL'
        else:
            return self._no_signal("Signal misaligned with EMA bias")
        
        # Step 4: Calculate entry, SL, TP
        entry_price = entry_data['close'].iloc[-1]
        
        if signal == 'BUY':
            stop_loss = smc_result['support']
            sl_distance = entry_price - stop_loss
            take_profit = entry_price + (sl_distance * self.rr_ratio)
        else:  # SELL
            stop_loss = smc_result['resistance']
            sl_distance = stop_loss - entry_price
            take_profit = entry_price - (sl_distance * self.rr_ratio)
        
        # Calculate confluence strength (0-100)
        strength = self._calculate_confluence_strength(smc_result)
        
        return {
            'signal': signal,
            'strength': strength,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'sl_distance': sl_distance,
            'rr_ratio': self.rr_ratio,
            'details': {
                'bos': smc_result['bos'],
                'mss': smc_result['mss'],
                'ob': smc_result['ob'],
                'fvg': smc_result['fvg'],
                'liquidity_sweep': smc_result['liquidity_sweep'],
                'ema_bias': 'bullish' if bullish_bias else 'bearish',
                'ema_value': ema_value,
                'confluence_count': smc_result['confluence_count'],
                'entry_tf': self.entry_tf,
                'bias_tf': self.bias_tf,
            }
        }
    
    def _check_smc_entry(self, data: pd.DataFrame) -> Dict:
        """
        Check for SMC entry conditions.
        
        Returns:
            Dict with SMC components detected
        """
        result = {
            'signal': 'NONE',
            'type': None,
            'bos': False,
            'mss': False,
            'ob': False,
            'fvg': False,
            'liquidity_sweep': False,
            'confluence_count': 0,
            'support': None,
            'resistance': None,
        }
        
        # Check Break of Structure (BOS)
        bos_result = self._check_bos(data)
        if bos_result:
            result['bos'] = True
            result['type'] = bos_result['type']
            result['confluence_count'] += 1
        
        # Check Market Structure Shift (MSS)
        mss_result = self._check_mss(data)
        if mss_result:
            result['mss'] = True
            result['confluence_count'] += 1
        
        # Check Order Block (OB)
        ob_result = self._check_ob(data)
        if ob_result:
            result['ob'] = True
            result['confluence_count'] += 1
        
        # Check Fair Value Gap (FVG)
        fvg_result = self._check_fvg(data)
        if fvg_result:
            result['fvg'] = True
            result['confluence_count'] += 1
        
        # Check Liquidity Sweep
        ls_result = self._check_liquidity_sweep(data)
        if ls_result:
            result['liquidity_sweep'] = True
            result['confluence_count'] += 1
        
        # Determine signal: BOS + MSS + (OB || FVG || LS)
        has_core_signals = (result['bos'] and result['mss'])
        has_confluence = (result['ob'] or result['fvg'] or result['liquidity_sweep'])
        
        if has_core_signals and has_confluence:
            result['signal'] = 'VALID'
            result['support'] = ob_result.get('support') if ob_result else data['low'].iloc[-1]
            result['resistance'] = ob_result.get('resistance') if ob_result else data['high'].iloc[-1]
        
        return result
    
    def _check_bos(self, data: pd.DataFrame) -> Optional[Dict]:
        """
        Break of Structure: Price breaks above last 2 swing highs (bullish)
        or below last 2 swing lows (bearish).
        
        Returns:
            {'type': 'BULLISH'|'BEARISH'} or None
        """
        if len(data) < 3:
            return None
        
        # Get last swing highs/lows
        last_high = data['high'].iloc[-2]
        prev_high = data['high'].iloc[-3]
        last_low = data['low'].iloc[-2]
        prev_low = data['low'].iloc[-3]
        
        current_high = data['high'].iloc[-1]
        current_low = data['low'].iloc[-1]
        
        # Bullish BOS: Break above last 2 swing highs
        if current_high > last_high and last_high > prev_high:
            return {'type': 'BULLISH'}
        
        # Bearish BOS: Break below last 2 swing lows
        if current_low < last_low and last_low < prev_low:
            return {'type': 'BEARISH'}
        
        return None
    
    def _check_mss(self, data: pd.DataFrame) -> Optional[Dict]:
        """
        Market Structure Shift: Last candle closes higher than previous 2
        (bullish) or lower than previous 2 (bearish).
        
        Returns:
            {'type': 'BULLISH'|'BEARISH'} or None
        """
        if len(data) < 3:
            return None
        
        last_close = data['close'].iloc[-1]
        prev_close = data['close'].iloc[-2]
        prev_prev_close = data['close'].iloc[-3]
        
        # Bullish MSS
        if last_close > prev_close and prev_close > prev_prev_close:
            return {'type': 'BULLISH'}
        
        # Bearish MSS
        if last_close < prev_close and prev_close < prev_prev_close:
            return {'type': 'BEARISH'}
        
        return None
    
    def _check_ob(self, data: pd.DataFrame) -> Optional[Dict]:
        """
        Order Block: Bullish candle (with large wick) before bearish candle,
        or vice versa. Detects imbalance level.
        
        Returns:
            {'support'|'resistance': float} or None
        """
        if len(data) < 3:
            return None
        
        # Get last two candles
        curr_open = data['open'].iloc[-1]
        curr_close = data['close'].iloc[-1]
        prev_open = data['open'].iloc[-2]
        prev_close = data['close'].iloc[-2]
        prev_high = data['high'].iloc[-2]
        prev_low = data['low'].iloc[-2]
        
        # Bullish OB: Previous bullish candle (close > open) with lower wicks
        # Price returns to it as support
        if prev_close > prev_open and curr_close < prev_close:
            # OB level is near previous candle's low
            return {'support': prev_low}
        
        # Bearish OB: Previous bearish candle (close < open) with upper wicks
        # Price returns to it as resistance
        if prev_close < prev_open and curr_close > prev_close:
            # OB level is near previous candle's high
            return {'resistance': prev_high}
        
        return None
    
    def _check_fvg(self, data: pd.DataFrame) -> Optional[Dict]:
        """
        Fair Value Gap: Imbalance between 3 candles (candle 1 high < candle 3 low
        in uptrend, or candle 1 low > candle 3 high in downtrend).
        
        Returns:
            {'level': float, 'type': 'bullish'|'bearish'} or None
        """
        if len(data) < 4:
            return None
        
        # Get 3-candle imbalance
        c3_high = data['high'].iloc[-1]
        c3_low = data['low'].iloc[-1]
        c2_open = data['open'].iloc[-2]
        c2_close = data['close'].iloc[-2]
        c1_high = data['high'].iloc[-3]
        c1_low = data['low'].iloc[-3]
        
        # Bullish FVG: Gap up (C1 high < C2 close && C2 open < C3 low)
        if c1_high < c2_close and c2_open < c3_low:
            return {'level': (c1_high + c2_open) / 2, 'type': 'bullish'}
        
        # Bearish FVG: Gap down (C1 low > C2 close && C2 open > C3 high)
        if c1_low > c2_close and c2_open > c3_high:
            return {'level': (c1_low + c2_open) / 2, 'type': 'bearish'}
        
        return None
    
    def _check_liquidity_sweep(self, data: pd.DataFrame) -> Optional[Dict]:
        """
        Liquidity Sweep: Wick extends beyond previous swing high/low
        then closes back inside range.
        
        Returns:
            {'type': 'bullish'|'bearish'} or None
        """
        if len(data) < 3:
            return None
        
        curr_high = data['high'].iloc[-1]
        curr_low = data['low'].iloc[-1]
        curr_close = data['close'].iloc[-1]
        
        prev_high = data['high'].iloc[-2]
        prev_low = data['low'].iloc[-2]
        
        # Bullish Sweep: High extends above prev high, close inside
        if curr_high > prev_high and curr_close < prev_high:
            return {'type': 'bullish'}
        
        # Bearish Sweep: Low extends below prev low, close inside
        if curr_low < prev_low and curr_close > prev_low:
            return {'type': 'bearish'}
        
        return None
    
    def _calculate_ema(self, series: pd.Series, period: int) -> float:
        """Calculate EMA for last value."""
        if len(series) < period:
            return series.mean()
        return series.ewm(span=period, adjust=False).mean().iloc[-1]
    
    def _calculate_confluence_strength(self, smc_result: Dict) -> int:
        """Calculate signal strength based on confluence count (0-100)."""
        # Base strength from confluence
        confluence_scores = {
            1: 30,
            2: 60,
            3: 80,
            4: 95,
            5: 100,
        }
        base_score = confluence_scores.get(smc_result['confluence_count'], 50)
        return min(100, base_score)
    
    def _no_signal(self, reason: str = "") -> Dict:
        """Return no signal."""
        return {
            'signal': 'NONE',
            'strength': 0,
            'entry_price': None,
            'stop_loss': None,
            'take_profit': None,
            'details': {
                'reason': reason,
                'confluence_count': 0,
            }
        }
    
    def get_status(self) -> Dict:
        """Get strategy status."""
        return {
            'strategy': 'SMC',
            'enabled': True,
            'entry_timeframe': self.entry_tf,
            'bias_timeframe': self.bias_tf,
            'ema_period': self.ema_period,
            'rr_ratio': self.rr_ratio,
            'last_signal': self.last_signal,
            'total_signals': len(self.signal_history),
        }
