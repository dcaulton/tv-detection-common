from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

# Enums (as before)
class TuningType(enum.Enum):
    OTA = "OTA"
    IPTV = "IPTV"

class ChannelStatus(enum.Enum):
    UNKNOWN = "unknown"
    WORKING = "working"
    BROKEN = "broken"
    GEO_BLOCKED = "geo_blocked"

class RecordingStatus(enum.Enum):
    PENDING = "pending"
    RECORDING = "recording"
    COMPLETED = "completed"
    FAILED = "failed"

# Channel table (as before)
class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tuning_type = Column(Enum(TuningType), nullable=False)
    tuning_details = Column(JSON, nullable=False)  # {"url": "..."} or {"channel_number": "2.1"}

    epg_source = Column(String(512), nullable=True)

    group_category = Column(String(100), nullable=True)
    geo_blocked = Column(Boolean, default=False)
    vpn_country = Column(String(50), nullable=True)

    last_tested = Column(DateTime, nullable=True)
    status = Column(Enum(ChannelStatus), default=ChannelStatus.UNKNOWN)

    schedules = relationship("Schedule", back_populates="channel")
    scans = relationship("Scan", back_populates="channel")
    recording = relationship("Recording", back_populates="channel", uselist=False)

# Program table (rich metadata)
class Program(Base):
    __tablename__ = 'programs'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    episode_title = Column(String(255), nullable=True)
    season_number = Column(Integer, nullable=True)
    episode_number = Column(Integer, nullable=True)
    genre = Column(String(100), nullable=True)
    subcategory = Column(String(100), nullable=True)
    rating = Column(String(50), nullable=True)
    original_air_date = Column(DateTime, nullable=True)
    actors = Column(JSON, nullable=True)  # ["Actor1", "Actor2"]
    directors = Column(JSON, nullable=True)
    writers = Column(JSON, nullable=True)
    image_url = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    source = Column(String(100), nullable=True)

    schedules = relationship("Schedule", back_populates="program")

# Schedule table (program airing on channel)
class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
    program_id = Column(Integer, ForeignKey('programs.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    source = Column(String(100), nullable=True)

    channel = relationship("Channel", back_populates="schedules")
    program = relationship("Program", back_populates="schedules")
    recording = relationship("Recording", back_populates="schedule", uselist=False)

# Recording table (actual file capture)
class Recording(Base):
    __tablename__ = 'recordings'

    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey('schedules.id'), nullable=False)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
    program_id = Column(Integer, ForeignKey('programs.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    file_path = Column(String(512), nullable=True)
    status = Column(Enum(RecordingStatus), default=RecordingStatus.PENDING)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    schedule = relationship("Schedule", back_populates="recording")
    channel = relationship("Channel")
    program = relationship("Program")

# Scan table (validation logs)
class Scan(Base):
    __tablename__ = 'scans'

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
    tested_at = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, nullable=False)
    details = Column(Text, nullable=True)
    vpn_used = Column(String(50), nullable=True)

    channel = relationship("Channel", back_populates="scans")
