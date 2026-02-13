"""
Agregació de dades per jugador.
Principi SRP: Única responsabilitat d'agregar dades.
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class DataAggregator:
    """Agrega dades de jugadors."""
    
    @staticmethod
    def aggregate_by_player(df: pd.DataFrame, features: list,
                           player_id_col: str = 'player_feb_id',
                           player_name_col: str = 'player_name',
                           weighted: bool = True) -> pd.DataFrame:
        """
        Agrega dades per jugador amb mitjana ponderada per minuts jugats.
        
        MILLORA: Utilitza mitjana ponderada per minuts per donar més pes
        als partits amb més minuts jugats (més representatius del perfil del jugador).
        
        Args:
            df: DataFrame amb dades de jugadors
            features: Llista de característiques NORMALITZADES a agregar
            player_id_col: Columna amb ID del jugador
            player_name_col: Columna amb nom del jugador
            weighted: Si True, usa mitjana ponderada per minuts. Si False, mitjana simple.
            
        Returns:
            DataFrame agregat per jugador
        """
        if not weighted or 'minutes_played' not in df.columns:
            # Mitjana simple (comportament anterior)
            agg_dict = {col: 'mean' for col in features if col in df.columns}
            agg_dict[player_name_col] = 'first'
            if 'minutes_played' in df.columns:
                agg_dict['minutes_played'] = 'sum'
            
            df_agg = df.groupby(player_id_col).agg(agg_dict).reset_index()
            logger.info(f"Dades agregades (mitjana simple): {len(df)} registres -> {len(df_agg)} jugadors")
        else:
            # Mitjana ponderada per minuts
            def weighted_mean(group, features):
                result = {player_name_col: group[player_name_col].iloc[0]}
                total_minutes = group['minutes_played'].sum()
                
                for col in features:
                    if col in group.columns:
                        result[col] = (group[col] * group['minutes_played']).sum() / total_minutes
                
                result['minutes_played'] = total_minutes
                return pd.Series(result)
            
            df_agg = df.groupby(player_id_col).apply(
                lambda x: weighted_mean(x, features)
            ).reset_index()
            
            logger.info(f"Dades agregades (mitjana ponderada per minuts): {len(df)} registres -> {len(df_agg)} jugadors")
        
        return df_agg
    
    @staticmethod
    def aggregate_raw_stats(df: pd.DataFrame, 
                           raw_stats: list,
                           player_id_col: str = 'player_feb_id',
                           player_name_col: str = 'player_name') -> pd.DataFrame:
        """
        Agrega estadístiques RAW per jugador (suma total).
        
        Usar aquesta funció per agregar estadístiques sense normalitzar.
        
        Args:
            df: DataFrame amb dades de jugadors
            raw_stats: Llista d'estadístiques RAW a sumar
            player_id_col: Columna amb ID del jugador
            player_name_col: Columna amb nom del jugador
            
        Returns:
            DataFrame agregat amb totals
        """
        agg_dict = {col: 'sum' for col in raw_stats if col in df.columns}
        agg_dict[player_name_col] = 'first'
        agg_dict['num_games'] = 'size'  # Nombre de partits
        
        df_agg = df.groupby(player_id_col).agg(agg_dict).reset_index()
        
        logger.info(f"Estadístiques RAW agregades: {len(df)} registres -> {len(df_agg)} jugadors")
        return df_agg
    
    @staticmethod
    def aggregate_with_custom_functions(df: pd.DataFrame, 
                                       agg_dict: dict,
                                       group_by_col: str = 'player_feb_id') -> pd.DataFrame:
        """
        Agrega dades amb funcions personalitzades.
        
        Args:
            df: DataFrame
            agg_dict: Diccionari amb columnes i funcions d'agregació
            group_by_col: Columna per agrupar
            
        Returns:
            DataFrame agregat
        """
        df_agg = df.groupby(group_by_col).agg(agg_dict).reset_index()
        logger.info(f"Agregació personalitzada completada: {len(df_agg)} grups")
        return df_agg
